import argparse

from .noisyfit import noisy_fit
from         . import set_backend, get_backend, Backend

def _validate_outfile(s):
    if s[-4:].lower() not in ('.svg', '.png'):
        raise argparse.ArgumentTypeError('Output filename must case-insensitively end in ".svg" or ".png".')

    try:
        with open(s, 'w') as _:
            return s
    except:
        raise argparse.ArgumentTypeError('Unable to open "{}" with write permissions.'.format(s))


def _validate_rsq(s):
    try:
        x = float(s)
    except ValueError:
        raise argparse.ArgumentTypeError('"{}" is not a valid floating point value.'.format(s))

    if 0.0 < x < 1.0:
        return x

    raise argparse.ArgumentTypeError('r-squared values must be in the open interval (0,1).')


def _validate_backend(s):
    t = s.upper()
    if hasattr(Backend, t):
        attr = getattr(Backend, t)
        if isinstance(attr, Backend):
            try:
                set_backend(attr)
                return attr
            except ImportError:
                raise argparse.ArgumentTypeError('Backend "{}" is not available.'.format(s.upper()))

    raise argparse.ArgumentTypeError('"{}" is not a recognized backend.'.format(s))

def parse_args(argsIn=None):
    psr = argparse.ArgumentParser()
    psr.add_argument('coefficients', type=float, nargs=2, help='Coefficients a,b of template line y = a+b*x.')
    psr.add_argument('rsq', type=_validate_rsq, help='Target r-squared')
    psr.add_argument('steps', type=int, default=100, nargs='?', help='Number of points in data to fit. Defaults to 100.')
    psr.add_argument('--seed', help='RNG seed. If convertable to integer, it is. Note that the absolute value is taken '
                                    'of negative integers, so n and -n are the same seed.')
    psr.add_argument('--backend', type=_validate_backend,
                     help='Case-insensitive name of a member of the Backend enumerated type: '
                          '{}.'.format(','.join([i.name for i in Backend])))
    psr.add_argument('--outfile', '-o', type=_validate_outfile, help='Generate plots, and save to this file. '
                                                                     'Requires Matplotlib. PNG and SVG formats '
                                                                     'are supported, and selected by the file extension.')
    psr.add_argument('--quiet', '-q', action='store_true', help='Suppress the display of parameters.')

    args = psr.parse_args(argsIn)

    if not args.backend:
        args.backend = get_backend()

    return args


def echo_args(args):
    print('Backend:', args.backend)
    print('Coefficients:', args.coefficients)
    print('Target r-squared:', args.rsq)
    print('Number of points:', args.steps)
    print('RNG seed:', args.seed)

    if args.outfile:
        print('Output file:', args.outfile)

    print()


def decode_args(args):
    a,b = args.coefficients

    seed = args.seed
    if seed is not None:
        try:
            seed = int(seed)
        except ValueError:
            pass

    return dict(a=a, b=b, rsq=args.rsq, N=args.steps, seed=seed)

def main():
    args = parse_args()

    if not args.quiet:
        echo_args(args)

    params = noisy_fit(**decode_args(args))

    info = params['template']
    print('Template Line')
    print('-------------')
    print('Coefficients:', info.a, info.b)
    print('Mean:', info.data.mean)

    print('\nMixed Data')
    print('----------')
    print('Mean:', params['ydata'].mean)
    print('Noise Width:', params['noise_width'])

    info = params['fit']
    print('\nFitted Line')
    print('-----------')
    print('Coefficients:', info.a, info.b)
    print('Mean:', info.data.mean)
    print('R-squared:', info.rsq)

    if args.outfile:
        from   matplotlib.figure import Figure, SubplotParams
        import matplotlib

        fig = Figure(figsize=(6,4.5), subplotpars=SubplotParams(
            left=0.04, bottom=0.05, right=0.96, top=0.95))

        ax = fig.add_subplot(1,1,1, xticks=[], yticks=[])

        xdata = params['xdata']
        ydata = params['ydata']
        yTmpl = params['template'].data
        yFit  = params['fit'].data

        plots = ax.plot(xdata, ydata, 'k.', xdata, yTmpl, 'b', xdata, yFit, 'g', linewidth=1.0)

        plots[0].set_markersize(1)
        plots[1].set_alpha(0.5)
        plots[2].set_alpha(0.5)

        if args.outfile.lower().endswith('.svg'):
            from matplotlib.backends.backend_svg import FigureCanvas
            mpl_backend = 'svg'
            file_mode = 'w'

        else:
            from matplotlib.backends.backend_agg import FigureCanvas
            mpl_backend = 'agg'
            file_mode = 'wb'

        matplotlib.use(mpl_backend)
        cvs = FigureCanvas(fig)

        with open(args.outfile, file_mode) as f:
            getattr(cvs, 'print_' + f.name[-3:].lower())(f)

if __name__ == '__main__':
    main()


import argparse
from random import Random

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

    if 0.0 < x <= 1.0:
        return x

    raise argparse.ArgumentTypeError('r-squared values must be in the half-open interval (0,1].')


def _validate_density(s):
    try:
        x = float(s)
    except ValueError:
        raise argparse.ArgumentTypeError('"{}" is not a valid floating point value.'.format(s))

    if 0.0 < x <= 1.0:
        return x

    raise argparse.ArgumentTypeError('Density values must be in the closed interval [0,1].')


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
    psr = argparse.ArgumentParser(description='Given a line and target r-squared, noisy data is generated and a line fit '
                                              'to them. A report is printed, and a plot-to-file feature is available.',
                                  epilog='The relative error of the obtained r-squared with repect to the target is '
                                         'included in the report. To decrease this error, set the target closer to one '
                                         'or increase the number of points.')
    psr.add_argument('coefficients', type=float, nargs=2, help='Coefficients a,b of input line y = a+b*x.')
    psr.add_argument('rsq', type=_validate_rsq, help='Target r-squared')
    psr.add_argument('steps', type=int, default=100, nargs='?', help='Number of points generated; defaults to 100.')
    psr.add_argument('--seed', help='RNG seed. If convertable to integer, it is. Note that the absolute value is taken '
                                    'of negative integers; n and -n are the same seed.')
    psr.add_argument('--backend', type=_validate_backend, help='Case-insensitive selection from: '
                                                               '{}.'.format(', '.join([i.name.lower() for i in Backend])))

    grp = psr.add_argument_group('plotting')
    grp.add_argument('--outfile', '-o', type=_validate_outfile, help='Generate plots, and save to this file. '
                                                                     'Requires Matplotlib. SVG and PNG formats '
                                                                     'are supported, and selected by the file extension.')
    grp.add_argument('--density', type=_validate_density, default=1.0, help='Noise density. Proportion of randomly '
                                                                            'distributed noisy points to plot. Defaults to 1.0.')

    args = psr.parse_args(argsIn)

    if not args.backend:
        args.backend = get_backend()

    return args


def decode_args(args):
    a,b = args.coefficients

    seed = args.seed
    if seed is not None:
        try:
            seed = int(seed)
        except ValueError:
            pass

    return ((a, b, args.rsq, args.steps), dict(rng=Random(seed)))


def main():
    args = parse_args()

    print('Starting Parameters')
    print('-------------------')
    print('Backend:', args.backend)
    print('Coefficients:', args.coefficients)
    print('Target r-squared:', args.rsq)
    print('Number of points:', args.steps)
    print('RNG seed:', args.seed)

    if args.outfile:
        print('Output file:', args.outfile)
        print('Noise density:', args.density)

    pargs, kwargs = decode_args(args)
    params = noisy_fit(*pargs, **kwargs)

    info = params['input']
    print('\nInput Line')
    print('----------')
    print('Coefficients:', info.a, info.b)
    print('Mean:', info.data.mean)

    print('\nMixed Data')
    print('----------')
    print('Mean:', params['ydata'].mean)
    print('Noise Width:', params['noise_width'])

    info = params['output']
    print('\nOutput Line')
    print('-----------')
    print('Coefficients:', info.a, info.b)
    print('Mean:', info.data.mean)
    print('R-squared:', info.rsq)
    print('Relative Error:', info.rsq/args.rsq - 1)

    if args.outfile:
        from   matplotlib.figure import Figure, SubplotParams
        import matplotlib

        fig = Figure(figsize=(6,4.5), subplotpars=SubplotParams(
            left=0.04, bottom=0.05, right=0.96, top=0.95))

        ax = fig.add_subplot(1,1,1, xticks=[], yticks=[])

        xdata = params[ 'xdata']
        ydata = params[ 'ydata']
        yIn   = params[ 'input'].data
        yOut  = params['output'].data
        rng   = kwargs[   'rng']
        N     = args.steps

        ax.plot(xdata, yIn, 'b', xdata, yOut, 'g', linewidth=1.0, alpha = 0.5)

        drops = [int(round(N*rng.random(), 0)) for i in range(int(round((1.0-args.density)*N, 0)))]
        drops.sort(reverse=True)

        xdata, ydata = map(list, [xdata, ydata])

        for i in drops:
            del xdata[i]
            del ydata[i]

        ax.plot(xdata, ydata, 'k.', markersize=1.0)

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

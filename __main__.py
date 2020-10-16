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
    psr.add_argument('--seed', type=int, help='RNG seed')
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
    return dict(a=a, b=b, rsq=args.rsq, N=args.steps, seed=args.seed)

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
    print('R-squared:', params['fit'].rsq)

    info = params['fit']
    print('\nFitted Line')
    print('-----------')
    print('Coefficients:', info.a, info.b)
    print('Mean:', info.data.mean)


if __name__ == '__main__':
    main()

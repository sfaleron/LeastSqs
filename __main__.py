import argparse
from random import Random

from . import leastsqs, set_backend, get_backend, Backend

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
    psr.add_argument('--backend', type=_validate_backend,
                     help='Case-insensitive name of a member of the Backend enumerated type: '
                          '{}.'.format(','.join([i.name for i in Backend])))
    psr.add_argument('--seed', type=int, help='RNG seed')
    psr.add_argument('--steps', type=int, default=100, help='Number of points in data to fit.')
    psr.add_argument('--noise', type=float, default=0.2, help='Noise scale, relative to b in the equation of the template line.')
    psr.add_argument('coefficients', type=float, nargs=2, help='Coefficients a,b of template line y = a+b*x.')
    psr.add_argument('--quiet', '-q', action='count', default=0, help=
        'Suppress output. One count disables the display of parameters, two suppresses all output.')

    args = psr.parse_args(argsIn)

    if not args.backend:
        args.backend = get_backend()

    return args


def echo_args(args):
    print('Backend:', args.backend)
    print('Coefficients:', args.coefficients)
    print('Noise scale:', args.noise)
    print('RNG seed:', args.seed)
    print('Number of points:', args.steps)

def make_points(args):
    a,b = args.coefficients
    rng = Random(args.seed)
    N = args.steps

    noiseamp = b*args.noise

    xdata = range(N)
    ydata = [a+b*t + noiseamp * (rng.random() - 0.5) for t in xdata]

    return xdata, ydata

def main():
    args = parse_args()

    if not args.quiet:
        echo_args(args)

    coeffs, (rsq, ssr) = leastsqs(*make_points(args))

    if args.quiet<2:
        print('coefficients out:', coeffs)
        print('rsq,ssr:', rsq, ssr)

if __name__ == '__main__':
    main()

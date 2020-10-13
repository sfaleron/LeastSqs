
from numpy.random import default_rng
from numpy import arange

import argparse

from . import leastsqs

psr = argparse.ArgumentParser()
psr.add_argument('--seed', type=int)
psr.add_argument('--steps', type=int, default=100)
psr.add_argument('--noise-abs', type=float)
psr.add_argument('--noise-rel', type=float)
psr.add_argument('coefficients', type=float, nargs=2)

args = psr.parse_args()
N = args.steps
sclIn,offIn = args.coefficients

if args.noise_rel is None:
    if args.noise_abs is None:
        noiseamp = 1.0
    else:
        noiseamp = args.noise_abs
else:
    noiseamp = args.noise_rel * sclIn

print('noise:', noiseamp)
print('coefficients in: ', args.coefficients)

rng = default_rng(args.seed)

xdata = arange(N)
ydata = xdata*sclIn+offIn + noiseamp*(rng.random(N)-0.5)

(offOut, sclOut), (rsq, ssr) = leastsqs(xdata, ydata)

print('coefficients out:', [sclOut, offOut])
print('rsq,ssr:', rsq, ssr)

ssyy = (ydata**2).sum() - N*ydata.mean()**2
ssxx = (xdata**2).sum() - N*xdata.mean()**2

ssxy = (xdata*ydata).sum() - N*xdata.mean()*ydata.mean()

sclOut = ssxy/ssxx
rsq = ssxy*ssxy/ssxx/ssyy
ssr = ssyy-sclOut*ssxy
offOut = ydata.mean() - sclOut*xdata.mean()

print('coefficients out:', [sclOut, offOut])
print('rsq,ssr:', rsq, ssr)

import argparse
from random import Random

from . import leastsqs

psr = argparse.ArgumentParser()
psr.add_argument('--seed', type=int)
psr.add_argument('--steps', type=int, default=100)
psr.add_argument('--noise-abs', type=float)
psr.add_argument('--noise-rel', type=float)
psr.add_argument('coefficients', type=float, nargs=2)

args = psr.parse_args()
N = args.steps
offIn,sclIn = args.coefficients

if args.noise_rel is None:
    if args.noise_abs is None:
        noiseamp = 1.0
    else:
        noiseamp = args.noise_abs
else:
    noiseamp = args.noise_rel * sclIn

print('noise:', noiseamp)
print('coefficients in: ', args.coefficients)

rng = Random(args.seed)

xdata = range(N)
ydata = [sclIn*t+offIn + noiseamp*(rng.random()-0.5) for t in xdata]

(offOut, sclOut), (rsq, ssr) = leastsqs(xdata, ydata)

print('coefficients out:', [offOut, sclOut])
print('rsq,ssr:', rsq, ssr)

xmean = sum(xdata) / N
ymean = sum(ydata) / N

ssxx = sum([i**2 for i in xdata]) - N*xmean**2
ssyy = sum([i**2 for i in ydata]) - N*ymean**2

ssxy = sum([i*j for i,j in zip(xdata, ydata)]) - N*xmean*ymean

sclOut = ssxy/ssxx
rsq = ssxy*ssxy/ssxx/ssyy
ssr = ssyy-sclOut*ssxy
offOut = ymean - sclOut*xmean

print('coefficients out:', [offOut, sclOut])
print('rsq,ssr:', rsq, ssr)

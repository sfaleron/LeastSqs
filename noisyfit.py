
from collections import namedtuple
from random import Random

from . import leastsqs

YInfo = namedtuple('YInfo', 'a b rsq data')


class Data(tuple):
    def __new__(cls, it):
        seq = tuple(it)

        o = super().__new__(cls, seq)
        o.mean = sum(seq)/len(seq)
        o.ss = sum([i**2 for i in seq]) - len(seq)*o.mean**2
        o.var = o.ss/len(seq)

        return o


def noisy_fit(aIn, bIn, rsqIn, N, rng=None, seed=None):
    if rng is None:
        rng = Random(seed)

    xdata = Data(range(N))

    yTmpl = Data([aIn+bIn*t for t in xdata])

    # variance of the mixed ydata is the sum of the variances of the input ydata and of the noise.
    # the variance of the noise is width^2/12.

    # this math is approximate, the formulae really apply to the mixed data, not the input parameters here.
    # empirically, the relative error in rsq is pretty small unless N and the target are both low.

    noise_width = (12*(bIn*bIn*xdata.ss/rsqIn/N - yTmpl.var))**.5

    ydata = Data([t + noise_width*(rng.random()-0.5) for t in yTmpl])

    (aFit, bFit), (rsqFit, ssr) = leastsqs(xdata, ydata)

    yFit = Data([aFit+bFit*t for t in xdata])

    return dict(xdata=xdata, ydata=ydata, noise_width=noise_width,
                input=YInfo(aIn,bIn,rsqIn, yTmpl), output=YInfo(aFit, bFit, rsqFit, yFit))

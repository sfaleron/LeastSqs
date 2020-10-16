
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


def noisy_fit(a, b, rsq, N, rng=None, seed=None):
    if rng is None:
        rng = Random(seed)

    xdata = Data(range(N))

    yTmpl = Data([a+b*t for t in xdata])

    # variance of the ydata is the sum of the variances of the template ydata and of the noise.
    # the variance of the noise is width^2/12.

    noise_width = (12*(b*b*xdata.ss/rsq/N - yTmpl.var))**.5

    ydata = Data([t + noise_width*(rng.random()-0.5) for t in yTmpl])

    (aFit, bFit), (rsqFit, ssr) = leastsqs(xdata, ydata)

    yFit = Data([aFit+bFit*t for t in xdata])

    return dict(xdata=xdata, ydata=ydata, noise_width=noise_width,
                template=YInfo(a,b,rsq, yTmpl), fit=YInfo(aFit, bFit, rsqFit, yFit))

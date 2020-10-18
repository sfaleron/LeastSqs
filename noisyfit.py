
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
    # variance of the ymixed data is a tricky function of the input parameters that follows straightforwardly enough
    # from a few of the equations at https://mathworld.wolfram.com/CorrelationCoefficient.html.

    # FIXME: The math is flawed, but approximately not-so-bad. The b-value that belongs is the fitted line's, not the
    # input parameter! I have renamed the variables to help prevent such confusions. The math and possibly input
    # parameters will be revised to be more correct or at least state assumptions explicitly.
    # It seems likely, for instance, that the mean of the ydata of the input line may be taken as the mean of all
    # three sets of ydata, which is really only a good approximation for sufficiently large N.

    noise_width = (12*(bIn*bIn*xdata.ss/rsqIn/N - yTmpl.var))**.5

    ydata = Data([t + noise_width*(rng.random()-0.5) for t in yTmpl])

    (aFit, bFit), (rsqFit, ssr) = leastsqs(xdata, ydata)

    yFit = Data([aFit+bFit*t for t in xdata])

    return dict(xdata=xdata, ydata=ydata, noise_width=noise_width,
                input=YInfo(aIn,bIn,rsqIn, yTmpl), output=YInfo(aFit, bFit, rsqFit, yFit))


from numpy import vstack, ones, fromiter

from collections import namedtuple

ForeignResult = namedtuple('ForeignResult', 'coeffs resids rank sings')


def _leastsqs(xdata, ydata, _foreign_implementation):
    xdata = fromiter(xdata, float)
    ydata = fromiter(ydata, float)

    if xdata.size != ydata.size:
        raise ValueError('xdata and ydata must be the same length.')

    size = ydata.size

    if size<2:
        raise ValueError('A minimum of two points is necessary.')

    data = vstack([xdata, ones(size)]).T
    result = ForeignResult(*_foreign_implementation(data, ydata, None))

    if result.rank == 1:
        raise ValueError('Input is underdetermined.')

    if size>2:
        ssyy = (ydata**2).sum() - size*ydata.mean()**2
        ssr = result.resids[0]

        # hopefully more numerically stable than 1.0-ssr/ssyy
        rsq = (ssyy-ssr)/ssyy
    else:
        rsq, ssr = 1.0, 0.0

    b, a = result.coeffs

    return (a, b), (rsq, ssr)

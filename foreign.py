
from numpy import vstack, ones, fromiter

def _leastsqs(xdata, ydata, _foreign_implementation):
    xdata = fromiter(xdata, float)
    ydata = fromiter(ydata, float)

    if xdata.size != ydata.size:
        raise ValueError('xdata and ydata must be the same length.')

    size = ydata.size

    if size<2:
        raise ValueError('A minimum of two points is necessary.')

    data = vstack([xdata, ones(size)]).T
    messy = _foreign_implementation(data, ydata, None)

    if size>2:
        ssyy = (ydata**2).sum() - size*ydata.mean()**2
        ssr = messy[1][0]

        # hopefully more numerically stable than 1.0-ssr/ssyy
        rsq = (ssyy-ssr)/ssyy
    else:
        rsq, ssr = 1.0, 0.0

    slope, offset = messy[0]

    return (slope, offset), (rsq, ssr)

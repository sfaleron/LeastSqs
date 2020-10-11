
try:
    from scipy.linalg import lstsq
except ImportError:
    from numpy.linalg import lstsq

from numpy import array, vstack, ones

def leastsqs(xdata, ydata):
    ydata = array(ydata)
    size = ydata.size

    if size<2:
        raise ValueError('A minimum of two points is necessary.')

    data = vstack([xdata, ones(size)]).T
    messy = lstsq(data, ydata, None)

    if size>2:
        ssyy = (ydata**2).sum() - size*ydata.mean()**2
        ssr = messy[1][0]

        # hopefully more numerically stable than 1.0-ssr/ssyy
        rsq = (ssyy-ssr)/ssyy
    else:
        rsq, ssr = 1.0, 0.0

    slope, offset = messy[0]

    return slope, offset, (rsq, ssr)

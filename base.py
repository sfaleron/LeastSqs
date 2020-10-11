
try:
    from scipy.linalg import lstsq
except ImportError:
    from numpy.linalg import lstsq

from numpy import array, vstack, ones

def leastsqs(xdata, ydata):
    ydata = array(ydata)
    size = ydata.size

    data = vstack([xdata, ones(size)]).T
    messy = lstsq(data, ydata, None)

    ssyy = (ydata**2).sum() - size*ydata.mean()**2
    ssr  = messy[1][0]

    rsq = 1.0-ssr/ssyy

    slope, off = messy[0]

    return slope, off, (rsq, ssr)

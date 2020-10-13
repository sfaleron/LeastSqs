
def leastsqs(xdata, ydata):
    xdata = tuple(xdata)
    ydata = tuple(ydata)

    xsize = len(xdata)
    ysize = len(ydata)

    if xsize != ysize:
        raise ValueError('xdata and ydata must be the same length.')

    size = xsize
    if size<2:
        raise ValueError('A minimum of two points is necessary.')

    xmean = sum(xdata)/size
    ymean = sum(ydata)/size

    ssxx = sum([i**2 for i in xdata]) - size*xmean**2
    ssyy = sum([i**2 for i in ydata]) - size*ymean**2

    ssxy = sum([i*j for i,j in zip(xdata,ydata)]) - size*xmean*ymean

    slope  = ssxy/ssxx
    offset = ymean-slope*xmean

    rsq = ssxy*ssxy/ssxx/ssyy
    ssr = ssyy-slope*ssxy

    return (slope, offset), (rsq, ssr)

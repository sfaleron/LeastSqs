
# Generate plots that illustrate the sample session from README.rst

# Uses matplotlib, so numpy is presumed.

# Supports vector/SVG and bitmap/PNG output, but normally only SVG is enabled.

SVG = True
PNG = True

from leastsqs import leastsqs
from numpy import arange, tan, pi
from collections import namedtuple

PlotSpec = namedtuple('PlotSpec', 'x y yfit')

STEPS = 100

tdata = arange(STEPS)/STEPS*2-1

specs = []

for i in (3,2,1):
    xdata = tdata*i*pi/8
    ydata = tan(xdata)
    a, b = leastsqs(xdata, ydata)[0]
    specs.append(PlotSpec(xdata, ydata, a+b*xdata))

from matplotlib.figure import Figure, SubplotParams

fig = Figure(figsize=(9,3), subplotpars=SubplotParams(
    left=.02, right=.98, wspace=.05, bottom=.05, top=.95))

axes = [fig.add_subplot(1,3,i, xticks=[], yticks=[]) for i in (1,2,3)]

for ax, spec in zip(axes, specs):
    ax.plot(spec.x, spec.y, spec.x, spec.yfit, 'g', linewidth=1.0)

import matplotlib

if SVG:
    matplotlib.use('svg')

    from matplotlib.backends.backend_svg import FigureCanvas

    cvs = FigureCanvas(fig)

    with open('sample_ses.svg', 'w') as f:
        cvs.print_svg(f)

if PNG:
    matplotlib.use('agg')

    from matplotlib.backends.backend_agg import FigureCanvas

    cvs = FigureCanvas(fig)

    with open('sample_ses.png', 'wb') as f:
        cvs.print_png(f)


# scipy is Most Preferred as a library of algorithms, while numpy's role here is historical, and is more properly
# considered as the data type under the hood. OTOH, numpy is considerably less bulky and much more widely installed.

# That reasoning applies all the moreso with respect to the native Python implementation. In a lot of cases, performance
# will be completely adequate, but it seems a waste not to use numerical libraries that are optimized and well-tested
# when available.

# There is a performance hit on startup if redundant large packages are imported. This may be remedied in the future.

# See also
# https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
# http://mathworld.wolfram.com/CorrelationCoefficient.html
# http://mathworld.wolfram.com/LeastSquaresFitting.html
# numpy book, chapter 10, section 1

try:
    from .base import leastsqs
except ImportError:
    from .native import leastsqs

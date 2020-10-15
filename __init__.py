
# scipy is Most Preferred as a library of algorithms, while numpy's role here is historical, and is more properly
# considered as the data type under the hood. OTOH, numpy is considerably less bulky and much more widely installed.

# That reasoning applies all the moreso with respect to the native Python implementation. In a lot of cases, performance
# will be completely adequate, but it seems a waste not to use numerical libraries that are optimized and well-tested
# when available.

# See also
# https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
# http://mathworld.wolfram.com/CorrelationCoefficient.html
# http://mathworld.wolfram.com/LeastSquaresFitting.html
# numpy book, chapter 10, section 1

# The discussion in the example section of scipy's documentation is much easier to follow, and applies to both!
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lstsq.html#scipy.linalg.lstsq

# The page https://mathworld.wolfram.com/CorrelationCoefficient.html seems to have an error. Eqs 52 and 54 cannot
# both be correct. 54 seems to be the mistaken one. It doesn't seem to have an impact on subsequent expressions,
# which could explain why it hasn't been caught/corrected.


from .core import Backend, set_backend, leastsqs

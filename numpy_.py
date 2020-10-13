
from functools import partial

from numpy.linalg import lstsq

from .foreign import _leastsqs

leastsqs = partial(_leastsqs, _foreign_implementation=lstsq)

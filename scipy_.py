
from functools import partial

from scipy.linalg import lstsq

from .foreign import _leastsqs

leastsqs = partial(_leastsqs, _foreign_implementation=lstsq)

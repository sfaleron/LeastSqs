
Introduction
============


NumPy_ and SciPy_ have algorithms that solve generalizations of this problem, but using them is an ordeal for the simple case of fitting a line to a collection of points on the plane. Also, the returned results do not include the commonly used "correlation coefficient".

This package provides a simple interface to these libraries for this usage and also provides a native implementation, so there are no required dependencies.

----

Usage
=====

Backend
-------

By default, the first time ``leastsqs()`` is invoked, a backend is selected. If ``scipy`` is found, it is selected. If not, then ``numpy`` is attempted. If neither are importable, the native backend is used.

To explicitly choose a backend, call the ``set_backend()`` function with a member of the ``Backend`` enumerated type, or the case-insensitive name (``SCIPY``, ``NUMPY``, or ``NATIVE``) of a member. ::

  from leastsqs import leastsqs, set_backend, Backend
  set_backend(Backend.NUMPY)

Equivalently:

::

  set_backend('NUMPY')

::

  set_backend('numpy')

::

  set_backend('NumPy')

The backend can be (re)set as often as desired. Note that the ``leastsqs()`` binding does not change; future calls will observe a successful change. ``ImportError`` is raised if the backend is not available.

----

Invoking
--------

**Call Signature**

::

  (a, b), (rsq, ssr) = leastsqs(xdata, ydata)

Where:

- ``xdata``, ``ydata`` are finite iterables of equal length, which can be no less than two. Any type that reasonably resolves to float should be fine, such as ``Decimals`` or ``Fractions``.

- ``(a, b)`` are the coefficients to a degree-one polynomial representing the fitted line, with equation ``y = a + b * x``.

- ``rsq``, r-squared, is the correlation coefficient. Consult the links below for details, but a value closer to one represents a better fit.

- ``ssr``, sum of squared residuals, is a more direct expression of the difference between the fitted line and the ydata.

**Sample Session**

To deterministically and with minimal arbitrariness generate sample data, we use the ``tan()`` function to represent a "noisy" line. Three iterations are presented, zooming progressively out to less-fitting ranges. ::

  >>> from math import tan,pi
  >>> from leastsqs import leastsqs

  >>> xmin, xmax, steps = -pi/8, pi/8, 100
  >>> xdata=[i/steps*(xmax-xmin)+xmin for i in range(steps)]
  >>> ydata=map(tan, xdata)

  >>> leastsqs(xdata,ydata)
  ((-8.837989025825217e-05, 1.0322804209108654), (0.9998037995453566, 0.0010748198836298764))

  >>> xmin, xmax = -pi/4, pi/4
  >>> xdata=[i/steps*(xmax-xmin)+xmin for i in range(steps)]
  >>> ydata=map(tan, xdata)

  >>> leastsqs(xdata,ydata)
  ((-0.0009640493561273813, 1.1504929684053804), (0.9959372422450656, 0.11101252195673025))

  >>> xmin, xmax = -3*pi/8, 3*pi/8
  >>> xdata=[i/steps*(xmax-xmin)+xmin for i in range(steps)]
  >>> ydata=map(tan, xdata)

  >>> leastsqs(xdata,ydata)
  ((-0.006716221015448294, 1.479157572162902), (0.9639490882609485, 3.7851982661489854))

----

See Also
========

| `"Least Squares Fitting" at Wolfram MathWorld <https://mathworld.wolfram.com/LeastSquaresFitting.html>`_
| `"Correlation Coefficient" at Wolfram MathWorld <https://mathworld.wolfram.com/CorrelationCoefficient.html>`_

.. _NumPy: https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq
.. _SciPy: https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lstsq.html#scipy.linalg.lstsq

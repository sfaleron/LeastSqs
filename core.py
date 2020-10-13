
from enum import Enum

Implementation = Enum('Implementation', 'SCIPY NUMPY NATIVE')

_implementation = [None]

def use(choice):
    resolved_choice = None
    if isinstance(choice, Implementation):
        resolved_choice = choice
    else:
        if isinstance(choice, str):
            choice = choice.upper()
            if hasattr(Implementation, choice):
                choice = getattr(Implementation, choice)
                if isinstance(choice, Implementation):
                    resolved_choice = choice

    if resolved_choice is None:
        raise ValueError(
            'Choice must be a member of the Implementation enumerated type: {}; '
            'or a case-insensitive string matching a member name.'.format(
                ','.join([i.name for i in Implementation])))
    else:
        if choice is Implementation.SCIPY:
            from .scipy_ import leastsqs
        if choice is Implementation.NUMPY:
            from .numpy_ import leastsqs
        if choice is Implementation.NATIVE:
            from .native import leastsqs

        _implementation[0] = leastsqs


def leastsqs(xdata, ydata):
    if _implementation[0] is None:
        try:
            use(Implementation.SCIPY)
        except ImportError:
            try:
                use(Implementation.NUMPY)
            except ImportError:
                use(Implementation.NATIVE)

    return _implementation[0](xdata, ydata)

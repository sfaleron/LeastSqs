
_backend = [None]


from enum import Enum

Backend = Enum('Backend', 'SCIPY NUMPY NATIVE')


def set_backend(choice):
    resolved_choice = None
    if isinstance(choice, Backend):
        resolved_choice = choice
    else:
        if isinstance(choice, str):
            choice = choice.upper()
            if hasattr(Backend, choice):
                choice = getattr(Backend, choice)
                if isinstance(choice, Backend):
                    resolved_choice = choice

    if resolved_choice is None:
        raise ValueError(
            'Choice must be a member of the Backend enumerated type: {}; '
            'or a case-insensitive string matching a member name.'.format(
                ','.join([i.name for i in Backend])))
    else:
        if choice is Backend.SCIPY:
            from .scipy_ import leastsqs
        if choice is Backend.NUMPY:
            from .numpy_ import leastsqs
        if choice is Backend.NATIVE:
            from .native import leastsqs

        _backend[0] = leastsqs


def leastsqs(xdata, ydata):
    if _backend[0] is None:
        try:
            set_backend(Backend.SCIPY)
        except ImportError:
            try:
                set_backend(Backend.NUMPY)
            except ImportError:
                set_backend(Backend.NATIVE)

    return _backend[0](xdata, ydata)

from inspect import getargspec
from functools import wraps

__all__ = ['defk']

try:
    # python 2
    basestring
    items = dict.iteritems
except NameError:
    # python 3
    basestring = str
    items = dict.items


def defk(_as=None):
    """This is a decorator for functions that take a single dict argument. We call
    these keyword functions. Applying defk simplifies the argument-binding process
    and helps enforce required vs optional keys. This is an adaptation of
    Prismatic's `defnk` from their `plumbing` library for Clojure.

    As an example, the following conventional function:
    ```
    def simple_fn(d):
        return [d['a'], d['c']]
    ```
    can be written with defk like this:
    ```
    @defk
    def simple_fnk(a, c):
        return [a, c]
    ```

    If a key is missing, `KeyError` will be thrown, as with a normal dict.

    A parameter can have a default value to be supplied if not found in the dict:
    ```
    @defk
    def default_fnk(a=100):
        return a
    ```

    The defk decorator accepts one optional string parameter, `_as`; if supplied,
    the decorated function is passed the entire argument dict as a keyword argument
    of `_as`:
    ```
    @defk('everything')
    def as_fnk(a, everything):
        return [a, everything]

    > as_fnk({'a': 1, 'b': 99})
    [1, {'a': 1, 'b': 99}]
    ```

    Finally, the keyword function can also have a keyword-splat parameter (**k) that
    collects any remaining (unnamed) keys in the argument dict:
    ```
    @defk
    def splat_fnk(a, **rest):
        return [a, rest]

    > splat_fnk({'a': 1, 'b': 2, 'z': 99})
    [1, {'b': 2, 'z': 99}]
    ```
    """

    # If a decorator is just used "bare" (eg. @defk), it gets the function to be
    # decorated as an argument, and we return the decorated function.
    
    # However, if the decorator is passed a parameter, as in @defk('z'), the
    # parameter comes through, and we return a decorator that Python applies to the
    # function to be decorated.

    # Therefore, `_as` will always have a value, but its meaning depends on
    # whether it's a string (parameter) or a callable (decoratee).

    if not isinstance(_as, basestring):
        f = _as
        _as = None

    def decorator(f):
        argspec = getargspec(f)
        keys = argspec.args
        defaults = argspec.defaults or ()
        splat = argspec.keywords

        defaults_begin = len(keys) - len(defaults)

        @wraps(f)
        def F(d):
            args = []

            for i, x in enumerate(keys):
                if _as and x == _as:
                    args.append(d)
                    continue

                try:
                    args.append(d[x])
                except KeyError:
                    # Key's not in the dict, so see if it has a default,
                    # else let the KeyError bubble.
                    if i >= defaults_begin:
                        args.append(defaults[i - defaults_begin])
                        continue
                    else:
                        raise

            if splat:
                rest = {k: v for k, v in items(d)
                        if k not in keys}
                return f(*args, **rest)
            else:
                return f(*args)

        return F

    if _as:
        return decorator
    else:
        return decorator(f)



@defk
def test_simple(x, y):
    """
    >>> test_simple({'x':1, 'y':5, 'z':10})
    6
    >>> test_simple({'x':5})
    Traceback (most recent call last):
        ...
    KeyError: 'y'
    """
    return x + y

@defk
def test_defaults(x, y, z=10):
    """
    >>> test_defaults({'x':1, 'y':5})
    16
    >>> test_defaults({'x':1, 'y':5, 'z':2})
    8
    """
    return x + y + z

@defk
def test_splat(x, **y):
    """
    >>> r = test_splat({'x':1, 'a':5, 'b':3})
    >>> r[0] == 1
    True
    >>> r[1] == {'a':5, 'b':3}
    True
    """
    return [x, y]

@defk('z')
def test_as_and_splat(x, z, **y):
    """
    >>> r = test_as_and_splat({'x':1, 'y':2, 'c':5})
    >>> r[0] == 1
    True
    >>> r[1] == {'x':1, 'y':2, 'c':5}
    True
    >>> r[2] == {'y':2, 'c':5}
    True
    """
    return [x, z, y]

@defk('whole')
def test_complex(a, c, whole, r=101, **k):
    """
    >>> m = {'a':1, 'c':5, 'f':9}
    >>> r = test_complex(m)
    >>> r[:2] == [1, 5]
    True
    >>> r[3:] == [101, {'f': 9}]
    True
    >>> r[2] == m
    True
    """
    return [a, c, whole, r, k]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

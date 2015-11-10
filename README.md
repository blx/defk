# defk

*Note: this is an alpha release*

`defk` is a decorator for making functions that take a single dict parameter.

Applied to a function `f(a, b, ...)`, `defk` returns a function `g(d)` that takes
a single dict `d`, extracts the keys corresponding to the params of `f`, and calls
`f` with the values of those keys bound to the params of `f`,
ie. `f(a=d[a], b=d[b], ...)`.

Applying defk simplifies the argument-binding process
and helps enforce required vs optional keys with less boilerplate.

`defk` is adapted from `defnk` in Prismatic's [plumbing][] library for Clojure.

[plumbing]: https://github.com/Prismatic/plumbing/tree/master/src/plumbing/fnk


## Examples

The following conventional function:

```python
def simple_fn(d):
    return [d['a'], d['c']]
```

can be written with `defk` like this:

```python
from defk import defk

@defk
def simple_fnk(a, c):
    return [a, c]

>>> simple_fnk({'a': 1, 'c': 5, 'm': 'ignored'})
[1, 5]
```

If a key is missing, `KeyError` will be raised, as with a normal dict.

A parameter can have a default value to be supplied if not found in the dict:
```python
@defk
def default_fnk(a=100):
    return a
```

The defk decorator accepts one optional string parameter, `_as`; if supplied,
the decorated function is passed the entire argument dict as a keyword argument
of `_as`:

```python
@defk('everything')
def as_fnk(a, everything):
    return [a, everything]

>>> as_fnk({'a': 1, 'b': 99})
[1, {'a': 1, 'b': 99}]
```

Finally, the keyword function can also have a keyword-splat parameter (`**k`) that
collects any remaining (unnamed) keys in the argument dict:

```python
@defk
def splat_fnk(a, **rest):
    return [a, rest]

>>> splat_fnk({'a': 1, 'b': 2, 'z': 99})
[1, {'b': 2, 'z': 99}]
```


## Rationale

__Why not just use the keyword splat, `f(**d)`?__

The `**` operator works beautifully in many cases, but gets sticky when the dict has
extra keys. It also doesn't provide a very useful message in the case of missing
keys, whereas `defk` will raise a KeyError containing the name of the missing key.

If you don't need access to the entire dict via `_as`, then the following can
generally be substituted for `defk`:

```python
>>> d = {'a':1, 'b':2, 'extra':5}

# If only a subset of the dict is requested:
>>> f = lambda a, b, c=10: [a, b, c]
>>> f(**{k: v for k, v in d.items() if k in inspect.getargspec(f).args})
[1, 2, 10]

# Splat soaks up surplus keywords:
>>> g = lambda a, **rest: ...
>>> g(**d)
[1, {'b':2, 'extra':5}]
```

However ... `defk` will be more useful with nested destructuring:

## TODO

For feature parity with Prismatic's `defnk`, `defk` still needs to
support **nested bindings**.


## Compatibility

`defk` is tested on Python 2.7 and 3.5 and has no external dependencies.

Tests are included (using `doctest`), and can be run by calling `python defk.py -v`.


## Licence

**The ISC License**

Copyright (c) 2015 Ben Cook

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

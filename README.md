# defk

*Note: this is an alpha release*

`defk` is a decorator for functions that take a single dict argument.
Applying defk simplifies the argument-binding process
and helps enforce required vs optional keys with less boilerplate.

`defk` is adaptated from `defnk` in Prismatic's [plumbing][] library for Clojure.

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


## TODO

For feature parity with Prismatic's `defnk`, `defk` still needs to
support **nested bindings**.


## Compatibility

`defk` is tested on Python 2.7 and 3.5 and has no external dependencies.

Tests are included (using `doctest`), and can be run by calling `defk._tests()`.


## Licence

**The ISC License**

Copyright (c) 2015 Ben Cook

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

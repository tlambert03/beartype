#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2020 Cecil Curry.
# See "LICENSE" for further details.

'''
**Beartype object utilities.**

This private submodule implements supplementary object-handling utility
functions required by various :mod:`beartype` facilities, including callables
generated by the :func:`beartype.beartype` decorator.

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                           }....................
# ....................{ COSTANTS                          }....................
SENTINEL = object()
'''
Sentinel object of arbitrary value.

This object is internally leveraged by various utility functions to identify
erroneous and edge-case input (e.g., iterables of insufficient length).
'''

# ....................{ TESTERS                           }....................
# Note that this tester function *CANNOT* be memoized by the @callable_cached
# decorator, which requires all passed parameters to already be hashable.
def is_object_hashable(obj: object) -> bool:
    '''
    ``True`` only if the passed object is **hashable** (i.e., passable to the
    builtin :func:`hash` function *without* raising an exception and thus
    usable in hash-based containers like dictionaries and sets).

    Parameters
    ----------
    obj : object
        Object to be inspected.

    Returns
    ----------
    bool
        ``True`` only if this object is hashable.
    '''

    # Attempt to hash this object. If doing so raises *any* exception
    # whatsoever, this object is by definition unhashable.
    #
    # Note that there also exists a "collections.abc.Hashable" superclass.
    # Sadly, this superclass is mostly useless for all practical purposes. Why?
    # Because user-defined classes are free to subclass that superclass
    # despite overriding the __hash__() dunder method implicitly called by the
    # builtin hash() function to raise exceptions: e.g.,
    #
    #     from collections.abc import Hashable
    #     class HashUmUp(Hashable):
    #         def __hash__(self):
    #             raise ValueError('uhoh')
    #
    # Note also that we catch all possible exceptions rather than merely the
    # standard "TypeError" exception raised by unhashable builtin types (e.g.,
    # dictionaries, lists, sets). Why? For the same exact reason as above.
    try:
        hash(obj)
    # If this object is unhashable, return false.
    except Exception:
        return False

    # Else, this object is hashable. Return true.
    return True

# ....................{ GETTERS                           }....................
def get_object_type(obj: object) -> type:
    '''
    Either the passed object if this object is a class *or* the class of this
    object otherwise (i.e., if this object is *not* a class).

    Note that this function *never* raises exceptions on arbitrary objects,
    since the :func:`type` builtin wisely returns itself when passed itself:
    e.g.,

        >>> type(type(type)) is type
        True

    Parameters
    ----------
    obj : object
        Object to be inspected.

    Returns
    ----------
    type
        Type of this object.
    '''

    return obj if isinstance(obj, type) else type(obj)

# ....................{ GETTERS ~ name                    }....................
def get_object_name_qualified(obj: object) -> str:
    '''
    **Fully-qualified name** (i.e., ``.``-delimited name prefixed by the
    declaring module) of either passed object if this object is a class *or*
    the class of this object otherwise (i.e., if this object is *not* a class).

    Parameters
    ----------
    obj : object
        Object to be inspected.

    Returns
    ----------
    str
        Fully-qualified name of the type of this object.
    '''

    # Type of this object.
    cls = get_object_type(obj)

    # Unqualified name of this type.
    cls_basename = get_object_name_unqualified(cls)

    # Fully-qualified name of the module defining this class if this class is
    # defined by a module *OR* "None" otherwise.
    cls_module_name = get_object_module_name_or_none(cls)

    # Return either...
    return (
        # The "."-delimited concatenation of this class basename and module
        # name if this module name exists.
        '{}.{}'.format(cls_module_name, cls_basename)
        if cls_module_name is not None else
        # This class basename as is otherwise.
        cls_basename
    )


def get_object_name_unqualified(obj: object) -> str:
    '''
    **Unqualified name** (i.e., non-``.``-delimited basename) of either passed
    object if this object is a class *or* the class of this object otherwise
    (i.e., if this object is *not* a class).

    Parameters
    ----------
    obj : object
        Object to be inspected.

    Returns
    ----------
    str
        Unqualified name of this class.
    '''

    # Elegant simplicity diminishes aggressive tendencies.
    return get_object_type(obj).__name__

# ....................{ GETTERS ~ name : module           }....................
def get_object_module_name_or_none(obj: object) -> (str, None):
    '''
    **Fully-qualified name** (i.e., ``.``-delimited name prefixed by the
    declaring package) of the module declaring either the passed object if this
    object is a class *or* the class of this object otherwise (i.e., if this
    object is *not* a class) if this class declares a ``__module__`` dunder
    attribute *or* ``None`` otherwise.

    Parameters
    ----------
    obj : object
        Object to be inspected.

    Returns
    ----------
    (str, type(None))
        Either:

        * Fully-qualified name of the module declaring the type of this object
          if this type declares a ``__module__`` dunder attribute.
        * ``None`` otherwise.
    '''

    # Make it so, ensign.
    return getattr(get_object_type(obj), '__module__', None)

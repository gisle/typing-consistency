from typing import *
from typing import _TypedDictMeta
from types import FunctionType
from abc import ABCMeta
import collections.abc

class NYI(Exception):  # Not Yet Implemented
    pass

def isconsistent(obj: object, type_hint: Any) -> bool:
    """Check if the given object is consistent with the given
    PEP 484 type hint.  For classes and built in types it will
    work the same as ininstance().
    """

    if type_hint is Any:
        return True

    if type_hint is NoReturn:
        return False

    # Test for a NewType wrapper
    if type(type_hint) is FunctionType and hasattr(type_hint, '__supertype__'):
        type_hint = type_hint.__supertype__

    if type_hint is None:
        type_hint = type(None)

    if type(type_hint) is type or type(type_hint) is ABCMeta:
        if type_hint is float:
            type_hint = (float, int)
        elif type_hint is complex:
            type_hint = (complex, float, int)
        return isinstance(obj, type_hint)

    if origin := get_origin(type_hint):
        args = get_args(type_hint)

        if origin is Union:
            for t in args:
                if isconsistent(obj, t):
                    return True
            return False

        if origin is Literal:
            for lit in args:
                if type(obj) is type(lit) and obj == lit:
                    return True
            return False

        if type(origin) is type or type(origin) is ABCMeta:
            if not isinstance(obj, origin):
                return False

            if (origin is list or
                origin is set or
                (origin is tuple and len(args) == 2 and args[1] is ...) or
                origin is collections.abc.Sequence
            ):
                for e in obj:
                    if not isconsistent(e, args[0]):
                        return False
                return True

            if (origin is dict or
                origin is collections.abc.Mapping
            ):
                for k,v in obj.items():
                    if not isconsistent(k, args[0]):
                        return False
                    if not isconsistent(v, args[1]):
                        return False
                return True

            if origin is tuple:
                if len(args) == 1 and args[0] == ():  # Empty tuple type
                    args = ()
                if len(obj) != len(args):
                    return False
                for i in range(len(args)):
                    if not isconsistent(obj[i], args[i]):
                        return False
                return True

            if origin is type:
                # XXX handle Type[Union[X, Y]]
                # XXX handle Type[Any]
                if issubclass(obj, args[0]):
                    return True
                return False

            raise(NYI(f"Can't handle base origin {origin} yet"))

        raise(NYI(f"Can't handle origin {origin} yet"))

    if type(type_hint) is _TypedDictMeta:
        if not isinstance(obj, dict):
            return False
        for k, v in get_type_hints(type_hint).items():
            # XXX Wait for https://github.com/python/cpython/pull/17214 to be able
            # to discover what keys are optional
            if k not in obj:
                return False
            if not isconsistent(obj[k], v):
                return False
        return True

    raise(NYI(f"Can't handle type hint {type_hint} yet"))

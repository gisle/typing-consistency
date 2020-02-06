from typing import *
from typing import _TypedDictMeta
from types import FunctionType

class NYI(Exception):  # Not Yet Implemented
    pass

def isconsistent(obj: object, type_spec) -> bool:
    """Check if the given object is consistent with the given
    PEP 484 typespec.  For classes and built in types it will
    work the same as ininstance().
    """

    if type_spec is Any:
        return True

    # Test for a NewType wrapper
    if type(type_spec) is FunctionType and hasattr(type_spec, '__supertype__'):
        type_spec = type_spec.__supertype__

    if type(type_spec) is type:
        if type_spec is float:
            type_spec = (float, int)
        elif type_spec is complex:
            type_spec = (complex, float, int)
        return isinstance(obj, type_spec)

    if origin := get_origin(type_spec):
        args = get_args(type_spec)
        if origin is Union:
            for t in args:
                if isconsistent(obj, t):
                    return True
            return False
        elif origin is Literal:
            for lit in args:
                if type(obj) is type(lit) and obj == lit:
                    return True
            return False
        elif type(origin) is type:
            if not isinstance(obj, origin):
                return False
            if origin is list:
                for e in cast(list, obj):
                    if not isconsistent(e, args[0]):
                        return False
                return True
            elif origin is dict:
                for k,v in obj.items():
                    if not isconsistent(k, args[0]):
                        return False
                    if not isconsistent(v, args[1]):
                        return False
                return True
            elif origin is tuple:
                if len(args) == 2 and args[1] is ...:
                    for e in obj:
                        if not isconsistent(e, args[0]):
                            return False
                    return True
                if len(obj) != len(args):
                    return False
                for i in range(len(args)):
                    if not isconsistent(obj[i], args[i]):
                        return False
                return True
            else:
                raise(NYI(f"Can't handle base origin {origin} yet"))
        else:
            raise(NYI(f"Can't handle origin {origin} yet"))

    if type(type_spec) is _TypedDictMeta:  # XXX no better test for TypedDict?
        if not isinstance(obj, dict):
            return False
        for k, v in get_type_hints(type_spec).items():
            if k not in obj: # XXX check for __total__
                return False
            if not isconsistent(obj[k], v):
                return False
        return True

    raise(NYI(f"Can't evaluate type {type_spec} yet"))

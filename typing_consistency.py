from typing import *

class NYI(Exception):  # Not Yet Implemented
    pass

def isconsistent(obj: object, type_spec) -> bool:
    """Check if the given object is consistent with the given
    PEP 484 typespec.  For classes and built in types it will
    work the same as ininstance().
    """

    if type(type_spec) == type:
        return isinstance(obj, type_spec)

    if type_spec == Any:
        return True

    if origin := get_origin(type_spec):
        if not isinstance(obj, origin):
            return False
        args = get_args(type_spec)
        if origin == list:
            for e in cast(list, obj):
                if not isconsistent(e, args[0]):
                    return False
            return True
        elif origin == dict:
            for k,v in obj.items():
                if not isconsistent(k, args[0]):
                    return False
                if not isconsistent(v, args[1]):
                    return False
            return True
        elif origin == tuple:
            if len(obj) != len(args):
                return False
            for i in range(len(args)):
                if not isconsistent(obj[i], args[i]):
                    return False
            return True
        else:
            raise(NYI(f"Can't handle origin {origin} yet"))

    raise(NYI(f"Can't evaluate type {type_spec} yet"))

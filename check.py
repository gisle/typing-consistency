from typing import *
from typing_consistency import isconsistent

assert(isconsistent(None, object))
assert(isconsistent(None, Any))

assert(not isconsistent(None, List[int]))
assert(    isconsistent([],   List[int]))
assert(not isconsistent({},   List[int]))
assert(    isconsistent([1],  List[int]))
assert(not isconsistent([1,"foo"], List[int]))

assert(    isconsistent({}, Dict[str, int]))
assert(not isconsistent([], Dict[str, int]))
assert(    isconsistent({"foo": 1}, Dict[str, int]))

assert(    isconsistent((1, "foo"), Tuple[int, str]))

from datetime import date

class Person(TypedDict):
    first_name: str
    last_name: str
    born: Optional[date]

class Player(Person):
    score: int

assert(isconsistent({}, Person))
assert(isconsistent({'first_name': 'Joe', 'last_name': 'Smith'}, Person))

X = NewType("X", int)

assert(isconsistent(1, X))
assert(isconsistent("1", X))
assert(isconsistent(X(1), X))

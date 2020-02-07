import unittest

from typing_consistency import isconsistent

class BasicTests(unittest.TestCase):
    def testAny(self):
        from typing import Any
        self.assertTrue(isconsistent(None, Any))
        self.assertTrue(isconsistent({}, Any))
        self.assertTrue(isconsistent(int, Any))

    def testBasic(self):
        self.assertTrue(isconsistent(None, None))
        self.assertTrue(isconsistent(None, object))
        self.assertTrue(isconsistent(1, object))

        self.assertTrue(isconsistent(1, int))
        self.assertTrue(isconsistent(1, float))
        self.assertTrue(isconsistent(1.0, float))
        self.assertTrue(isconsistent(1, complex))
        self.assertTrue(isconsistent(1.0, complex))
        self.assertTrue(isconsistent("foo", str))
        self.assertTrue(isconsistent({}, dict))
        self.assertTrue(isconsistent([], list))

        class X: pass
        class Y(X): pass

        self.assertTrue(isconsistent(Y(), object))
        self.assertTrue(isconsistent(Y(), X))
        self.assertTrue(isconsistent(Y(), Y))

        # and some inconsistent ones
        self.assertFalse(isconsistent(1, None))
        self.assertFalse(isconsistent(1, str))
        self.assertFalse(isconsistent({}, list))
        self.assertFalse(isconsistent(X(), Y))

    def testNewType(self):
        from typing import NewType
        UID = NewType("UID", int)
        uid = UID(42)

        self.assertTrue(isconsistent(uid, UID))
        self.assertTrue(isconsistent(1, UID))

    def testList(self):
        from typing import List
        self.assertFalse(isconsistent(None, List[int]))
        self.assertTrue (isconsistent([],   List[int]))
        self.assertFalse(isconsistent({},   List[int]))
        self.assertTrue (isconsistent([1],  List[int]))
        self.assertFalse(isconsistent([1,"foo"], List[int]))

        from typing import Sequence
        self.assertFalse(isconsistent(None, Sequence[int]))
        self.assertTrue (isconsistent([],   Sequence[int]))
        self.assertFalse(isconsistent({},   Sequence[int]))
        self.assertTrue (isconsistent([1],  Sequence[int]))
        self.assertFalse(isconsistent([1,"foo"], Sequence[int]))

    def testDict(self):
        from typing import Dict
        self.assertTrue (isconsistent({}, Dict[str, int]))
        self.assertFalse(isconsistent([], Dict[str, int]))
        self.assertTrue (isconsistent({"foo": 1}, Dict[str, int]))
        self.assertFalse(isconsistent({"foo": "bar"}, Dict[str, int]))

        from typing import Mapping
        self.assertTrue (isconsistent({}, Mapping[str, int]))
        self.assertFalse(isconsistent([], Mapping[str, int]))
        self.assertTrue (isconsistent({"foo": 1}, Mapping[str, int]))
        self.assertFalse(isconsistent({"foo": "bar"}, Mapping[str, int]))

    def testSet(self):
        from typing import Set
        self.assertTrue (isconsistent(set(), Set[str]))
        self.assertFalse(isconsistent({}, Set[str]))
        self.assertTrue (isconsistent({"foo"}, Set[str]))
        self.assertTrue (isconsistent({1,2,3}, Set[int]))
        self.assertFalse(isconsistent({1,2,"foo"}, Set[int]))

    def testTuple(self):
        from typing import Tuple
        self.assertTrue (isconsistent((1, "foo"), Tuple[int, str]))
        self.assertFalse(isconsistent((1,),       Tuple[int, str]))
        self.assertFalse(isconsistent(("foo", 1), Tuple[int, str]))

        self.assertTrue(isconsistent((), Tuple[int, ...]))
        self.assertTrue(isconsistent((1,), Tuple[int, ...]))
        self.assertTrue(isconsistent((1,2), Tuple[int, ...]))
        self.assertTrue(isconsistent((1,2,3), Tuple[int, ...]))
        self.assertFalse(isconsistent((1,2,3,"foo"), Tuple[int, ...]))

        self.assertTrue(isconsistent((), Tuple[()]))
        self.assertFalse(isconsistent((1,), Tuple[()]))
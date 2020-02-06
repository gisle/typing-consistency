import unittest
from typing_consistency import isconsistent
from typing import Union, Optional, Literal

class UnionTests(unittest.TestCase):
    def testUnion(self):
        t = Union[int, str]
        self.assertFalse(isconsistent(None, t))
        self.assertTrue(isconsistent(1, t))
        self.assertTrue(isconsistent("foo", t))
        self.assertFalse(isconsistent(1.0, t))

        t = Optional[int]
        self.assertTrue(isconsistent(None, t))
        self.assertTrue(isconsistent(1, t))
        self.assertFalse(isconsistent("foo", t))

        class X: pass
        t = Optional[Union[float,X]]
        self.assertTrue(isconsistent(None, t))
        self.assertTrue(isconsistent(1, t))
        self.assertFalse(isconsistent("foo", t))

        t = Literal["x", "y"]
        self.assertTrue(isconsistent("y", t))
        self.assertFalse(isconsistent("z", t))
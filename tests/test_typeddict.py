import unittest
from typing_consistency import isconsistent
from typing import TypedDict

class T1(TypedDict):
    x: int
    y: int

class T2(T1, total=False):
    z: int

class T3(T2):
    foo: str 

class Movie(TypedDict):
    name: str
    year: int

class EmptyDict(TypedDict):
    pass

class TypedDictTests(unittest.TestCase):
    def testNamedDict(self):
        d = {
            'x': 1,
            'y': 1,
            'z': 2,
        }
        self.assertTrue(isconsistent({}, EmptyDict))
        self.assertFalse(isconsistent({}, T1))
        self.assertTrue(isconsistent(d, T1))
        self.assertTrue(isconsistent(d, T2))
        self.assertFalse(isconsistent(d, T3))

        d['foo'] = 4
        self.assertFalse(isconsistent(d, T3))
        d['foo'] = 'bar'
        self.assertTrue(isconsistent(d, T3))

        # TODO
        # del d['z']
        # self.assertTrue(isconsistent(d, T3))
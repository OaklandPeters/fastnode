"""
THis should be named 'logical.py' - but a version of that already exists.

@todo: Combine logical_node.py and logical.py
@todo: Test/decide on method for equality comparison __eq__
@todo: Add logical tests using other atoms

... maybe find unit-tests for booleans in pypy or something, and recreate them

"""
import operator

from node import FASTNode, fastnode, identity


class LogicalSyntax(object):

    def __and__(self, other):
        return type(self)(operator.__and__, self, other)

    def __or__(self, other):
        return type(self)(operator.__or__, self, other)

    def __invert__(self):
        # __not__ is not a normal Magic Method
        return type(self)(operator.__not__, self)



class LogicalNode(FASTNode, LogicalSyntax):
    """
    Interface: __call__
    """
    def __nonzero__(self):
        """Collapse, and check bool on result."""
        return bool(self())


class logical(fastnode):
    constructor = LogicalNode


import unittest

true = LogicalNode(identity, True)
false = LogicalNode(identity, False)
class Boolean_LogicalNodeTests(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(true)
        self.assertFalse(false)
    def test_or(self):
        self.assertTrue(true | False)
        self.assertTrue(true | True)
        self.assertTrue(true | true)
        self.assertFalse(false | False)
        self.assertTrue(true | false)
        self.assertTrue(false | true)
    def test_and(self):
        self.assertFalse(true & False)
        self.assertFalse(false & False)
        self.assertTrue(true & True)
        self.assertTrue(true & true)
        self.assertFalse(true & false)
        self.assertFalse(false & true)
    def test_compound(self):
        self.assertTrue(true | False & False)
        self.assertFalse((true | False) & False)


if __name__ == "__main__":
    unittest.main()

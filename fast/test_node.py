"""

Unit-tests and examples of syntax and behavior desired for AST-nodes.
"""
import unittest
import operator
import pdb

from .node import denode, FASTNode, NodeInterface

a, b, c = 5, 4, 2
inner = FASTNode(operator.__mul__, b, c)
outer = FASTNode(operator.__add__, a, inner)
# tree = FASTNode(
#     operator.__add__,
#     a,
#     FASTNode(
#         operator.__mul__,
#         b,
#         c
#     )
# )


class NodeTests(unittest.TestCase):

    def test_denode(self):
        self.assertEqual(denode(inner), 8)

    def test_nesting(self):
        self.assertEqual(inner(), outer.positional[1]())

    def test_basic(self):
        # 5 + 4 * 2
        standard_result = a + b * c

        # (+ 5 (* 4 2))
        operator_result = operator.__add__(
            a,
            operator.__mul__(
                b,
                c
            )
        )

        node_result = outer.__call__()  # evaluate via __call__

        self.assertEqual(node_result, operator_result)
        self.assertEqual(node_result, standard_result)

    def test_call(self):
        # Compare implicit VS explicit __call__
        self.assertEqual(
            inner(),
            inner.__call__()
        )
        self.assertEqual(
            outer(),
            outer.__call__()
        )
        self.assertEqual(denode(inner), inner())
        self.assertEqual(denode(outer), outer())

    def test_nonnested_denode(self):
        self.assertEqual(
            outer.positional[1]._denode(),
            8
        )

    def test_denode_function(self):
        self.assertEqual(
            denode(outer.positional[1]),
            8
        )

    def test_repr(self):
        self.assertIsInstance(repr(outer), str)
        self.assertEqual(repr(inner), "FASTNode::__mul__(4, 2)")


if __name__ == "__main__":
    unittest.main()

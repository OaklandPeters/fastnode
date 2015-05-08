"""

Analog to logical_node, but aiming at working on types



@todo: Bring in TypeCheckableMeta
@todo: TypeSyntax should inherit from LogicalSyntaxInterface
"""
import operator

from node import FASTNode, fastnode, identity, call_map, denode
from logical_node import LogicalSyntax



class TypeSyntax(LogicalSyntax):
    """
    Must coerce the rightmost value to the LogicalSyntax, so it can be mapped over.
    """

    def __and__(self, other):
        """
        @todo: This requires the Monad behavior that wrapping twice does nothing
            TypeSyntax(TypeSyntax(X)) ==> TypeSyntax(X)
        """
        return type(self)(operator.__and__, self, type(self)(other))

    def __or__(self, other):
        return type(self)(operator.__or__, self, type(self)(other))

    def __invert__(self):
        # __not__ is not a normal Magic Method
        return type(self)(operator.__not__, self)


def rec_map(obj, function):
    if isinstance(obj, TypeNode):
        return obj._rec_map(function)
    else:
        return obj


class TypeNode(FASTNode, TypeSyntax):
    """
    This needs the TypeCheckableMeta, so this works:
        typez = TypeNode(str) | None
    """
    def _rec_map(self, function):
        """Recursive mapper"""
        rec_mapper = lambda obj: rec_map(obj, function)
        # change self.function = function  ???????
        new_thing = call_map(rec_mapper, self.function, *self.positional, **self.keywords)


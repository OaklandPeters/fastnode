"""

The goal of this class is to provide the AST-like (Abstract Syntax Tree)
behavior portion of several logical and syntactic structures.
I find myself building these over and over again, and developing
a solid, abstacted version would save a lot of time.
... and be emotionally satisfying.


@todo: Add the recursive part
"""
# import operator
import abc
from collections import Mapping


def dict_map(function, mapping):
    if len(mapping) == 0:
        return {}
    # return {function(k:v) for k,v in Mapping.items(mapping)}
    return dict(map(function, *Mapping.items(mapping)))


def map_values(function, mapping):
    return dict_map(lambda key, value: (key, function(value)), mapping)


def call_map(mapper, function, *positional, **keywords):
    return function(
        # *[value for value in positional],
        *map(mapper, positional),
        # **{key:denode(value) for key, value in keywords.items()},
        # **dict_map(lambda key, value: (key, denode(value), keywords)
        **map_values(mapper, keywords)
    )


def denode(obj):
    if isinstance(obj, NodeInterface):
        return obj._denode()
    else:
        return obj


def call_denode(function, *positional, **keywords):
    return call_map(denode, function, *positional, **keywords)
    # return function(
    #     # *[value for value in positional],
    #     *map(denode, positional),
    #     # **{key:denode(value) for key, value in keywords.items()},
    #     **map_values(denode, keywords)
    # )


class FASTNode(object):
    """
    Faux Abstract Syntax Tree (FAST) node
    """
    def __init__(self, function, *positional, **keywords):
        self.function = function
        self.positional = positional
        self.keywords = keywords

    def _denode(self):
        return call_map(denode, self.function, *self.positional, **self.keywords)
#        return call_denode(self.function, *self.positional, **self.keywords)

    def __call__(self, *args, **kwargs):
        """
        Quandry: does this need seperate args/kwargs passed into it?
            ~ collapse, then __call__ on the result
        If not needed, _denode() could be merged in __call__, which would be
            a significant simplification

        """
        # return self._denode()(*args, **kwargs)
        return self._denode()

    def __repr__(self):
        return str.format(
            "{cls}::{fname}({args}{kwargs})",
            cls=type(self).__name__,
            fname=self.function.__name__,
            args=", ".join(repr(arg) for arg in self.positional),
            kwargs=", ".join("{0}={1}".format(k,repr(v)) for k,v in self.keywords.items())
        )

    def __eq__(self, other):
        if isinstance(other, FASTNode):
            return all([
                self.function == other.function,
                self.positional == other.positional,
                self.keywords == other.keywords
            ])
        else:
            return False



class NodeInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _denode(self):
        """
        Call this node's function, but recurse down the tree evaluating any
        Nodes in the positional and keyword arguments.
        """
        pass

    @abc.abstractmethod
    def __call__(self, *cargs, **ckwargs):
        pass

    @classmethod
    def __subclasscheck__(cls, subclass):
        if hasattr(subclass, "__call__") and hasattr(subclass, "_denode"):
            return True
        return False

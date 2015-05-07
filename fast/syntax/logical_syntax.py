import operator
from collections import Sequence, Callable


def printswitch(obj, indent):
    if hasattr(obj, indent):
        return obj.pprint(indent+1)
    else:
        return repr(obj)



class Node():
    def __new__(cls, *args):
        if len(args) == 1:  # unwrap when double wrapped
            if isinstance(args[0], Node):
                return args[0]
        else:
            object.__new__(cls, *args)

    def __init__(function, *terms):
        self.function = function
        self.terms = terms

    def __repr__(self):
        return self.pprint()

    def pprint(self, indent=0):
        return str.format(
            "{indent}Node< {func}:\n{terms}\n{indent}>",
            indent = " "*(4*indent),
            func   = printswitch(self.function, indent),
            terms  = printswitch(self.terms, indent)
        )

    def __call__(self, value):
        return self.function(*self.terms)(value)

    def __and__(self, other):
        return Node(operator.__and__, self, other)

    def __or__(self, other):
        return Node(operator.__or__, self, other)

    def __invert__(self):
        return Node(operator.__invert__, self)

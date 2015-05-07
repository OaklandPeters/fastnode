"""

Would really like to be able to say:

validate(value, Typez(str) & NonEmpty)
"""

from collections import Sequence, Callable
import functools



class TypeCheckableMeta(type):
    """
    ... basically has the TypeCheckable mixin behavior
    """
    # def __new__(mcls, name, bases, namespace):

    def __instancecheck__(cls, instance):
        if hasattr(cls, '__instancecheck__'):
            return cls.__instancecheck__(instance)
        else:
            return any(isinstance(instance, parent) for parent in cls.__bases__)

    def __subclasscheck__(cls, subclass):
        if hasattr(cls, '__subclasscheck__'):
            return cls.__subclasscheck__(subclass)
        else:
            return any(issubclass(subclass, parent) for parent in cls.__bases__)


class ValidationError(ValueError):
    pass

def validate(value, klass):
    if hasattr(klass, 'valid'):
        if not klass.valid(value):
            raise ValidationError(str.format(
                "Value of type {0} is not a valid {1}",
                type(value).__name__,
                klass.__name__
            ))
    else:
        if not isinstance(value, klass):
            raise TypeError(str.format(
                "Value of type {0} must be instance of {1}",
                type(value).__name__,
                klass.__name__
            ))

def isa(typez):
    @functools.wraps(isinstance)
    def wrapper(value):
        return isinstance(value, typez)
    return wrapper



class Typez(object):
    """
    Used like:
        Typez(predicate)


    Works sort of like defining a new class, but can be used a decorator inline.
    `predicate` can be several things:
        (1) a predicate callable: Type -> Boolean
        (2) a type object

    Returns a callable object (not another type)


    Aside: ... this looks like a monad


    @TODO: Seperate this into two portions.
        One - the logical portion I 've done elsewhere. class for inheritance
        Two - The part that makes this a decorator.j
    Make Two inherit from one
    """
    __metaclass__ = TypeCheckableMeta

    def __new__(cls, predicate):
        if isinstance(predicate, Typez):
            # If already a Typez, do nothing
            return predicate
        else:
            return object.__new__(cls, predicate)

    def __init__(self, predicate):
        self.predicate = predicate

    # This would be clearer with the clsproperty syntax
    @property
    def predicate(self):
        return self._predicate

    @predicate.setter
    def predicate(self, value):
        self._predicate = self.validate_predicate(value)

    @classmethod
    def validate_predicate(cls, predicate):
        if isinstance(predicate, Typez):
            return predicate
        elif isinstance(predicate, type):
            return lambda value: isinstance(value, predicate)
        elif isinstance(predicate, Callable):
            return predicate
        else:
            raise ValidationError("predicate must be a type or Callable.")


    # key function
    def __call__(self, value):
        return self.predicate(value)  # pylint: disable=E1102

    def __repr__(self):
        # Future function. Intention is to be able to print
        # the whole tree. (~this is very like an AST)
        # 
        # class Node():
        #   def __new__(cls, *args):
        #       if len(args) == 1:  # unwrap when double wrapped
        #           if isinstance(args[0], Node):
        #               return args[0]
        #       else:
        #           object.__new__(cls, *args)
        #   def __init__(function, *terms):
        #       self.function = function
        #       self.terms = terms
        #   def __repr__(self):
        #       return "Node< {0}: {1}".format(
        #           repr(self.function),
        #           repr(self.terms)
        #       )
        #   def __call__(self, value):
        #       return self.function(*self.terms)
        #   def 
        # 
        return repr(self.predicate)

    def __and__(self, other):
        return Typez(lambda value: self(value) and Typez(other))
    def __or__(self, other):
        return Typez(lambda value: self(value) or Typez(other))
    def __invert__(self):
        return Typez(lambda value: not self(value))




IsStr = Typez(str)
IsSeq = Typez(Sequence)
IsA = IsStr 


print()
print()
import pdb
pdb.set_trace()
print()

"""
FAST: Fake Abstract Syntax Tree

Recreation of AST-like behavior for use in constucting
syntactic DSLs for Python.

(~ monad like ... I think)
"""
from .node import FASTNode, denode, NodeInterface

__all__ = (
    'FASTNode',
    'denode',
    'NodeInterface'
)

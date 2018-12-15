import ast
from typing import Dict, Any

from pycodealizer.constants import LOAD_CONTEXT, STORE_CONTEXT, DEL_CONTEXT
from pycodealizer.entities.common import Module
from pycodealizer.exceptions import UnknownContextException
from pycodealizer.parsers.base import EntityParser


class IfParser(EntityParser):
    """Aggregates stats about if/ifelse/else conditionals."""

    def parse(self, node: Any, module: Module, context: Dict[str, Any]):
        """
        Add an if/else conditional to the module stats with details on the complexity
        of the condition and size of the if/else block.

        There are three fields an `ast.If` node has:
            - "test" holds a single node that describes the condition
            - "body" holds a list of nodes
            - "orelse" holds a list of nodes

        :param node: The node that represents a variable name to be added to the statistics.
        :param module: The python module where this variable is encountered.
        :param context: The context of the given node in the Abstract Syntax Tree.
        :return: ???
        """
        if isinstance(node.ctx, ast.Load):
            context[LOAD_CONTEXT] = True
        elif isinstance(node.ctx, ast.Store):
            context[STORE_CONTEXT] = True
        elif isinstance(node.ctx, ast.Del):
            context[DEL_CONTEXT] = True
        else:
            raise UnknownContextException(f'Unknown context {node.ctx.__class__.__name__}')

        module.add_variable(node.id, node.lineno, context)


if_parser = IfParser()

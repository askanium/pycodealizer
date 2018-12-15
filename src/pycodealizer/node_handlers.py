import ast

from pycodealizer.entities.common import Module
from pycodealizer.parsers.base import Parser


class ASTNodeHandler(ast.NodeVisitor):
    """Deals with various types of AST nodes."""

    def __init__(self):
        self.parser = Parser()

    def visit(self, node):
        method = 'handle_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def update_file_occurrence(self, path: str) -> None:
        """Set the new file occurrence path for the upcoming nodes."""
        self.parser.modules.append(Module(path))

    def handle_node(self, node):
        """Handles a given AST node and adds the corresponding stats to the statistics field."""
        method = 'handle_' + node.__class__.__name__
        self.parser.parse(node)
        visitor = getattr(self, method, lambda x: None)  # TODO remove this ugly lambda which was put temporarily here
        return visitor(node)

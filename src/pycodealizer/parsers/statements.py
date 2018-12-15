import ast
from typing import Any

from pycodealizer.entities.common import Module, Context
from pycodealizer.entities.statements import AssignmentEntity
from pycodealizer.parsers.base import EntityParser


class AssignmentParser(EntityParser):
    """Parses assignment nodes."""

    def parse(self, node: ast.Assign, module: Module, context: Context):
        """Process an `ast.Assign` node and extract relevant stats.

        An ``ast.Assign`` node has two fields:
            - ``targets`` that represents a list of nodes
            - ``value`` that is a single node that is assigned to targets

        :param node: The node that represents an assignment operation.
        :param module: The python module where this variable is encountered.
        :param context: The context of the given node.
        :return: The AssignmentEntity instance created from the given ``ast.Assign`` node.
        """
        assignment = AssignmentEntity(node)
        context.stack_ast_node(assignment)

        super().parse(node, module, context)

        context.unstack_ast_node()
        module.add_assignment(assignment)

        return assignment

    def parse_targets(self, targets: list, module: Module, context: Context):
        """Process the "targets" field of the ``ast.Assign`` node.

        Multiple targets represent assigning the same value to each.

        In case the target list consists of a single `tuple` object,
        then the assignment represents an unpacking of values.

        :param targets: The list of targets on the left side of the assignment.
        :param module: The python module where this variable is encountered.
        :param context: The context of the given node in the Abstract Syntax Tree.
        """
        assignment = context.current_ast_node

        for node in targets:
            parser = self.get_parser(node)
            target = parser.parse(node, module, context)
            assignment.add_target(target)

    def parse_value(self, value: Any, module: Module, context: Context):
        """Process the "value" field of the ``ast.Assign`` node.

        :param value: The node that is assigned / unpacked.
        :param module: The python module where this variable is encountered.
        :param context: The context of the given node in the Abstract Syntax Tree.
        """
        assignment = context.current_ast_node

        parser = self.get_parser(value)
        value_entity = parser.parse(value, module, context)

        assignment.add_value(value_entity)


assignment_parser = AssignmentParser()

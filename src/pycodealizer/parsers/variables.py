import ast
from typing import Any

from pycodealizer.entities.common import Module, Context
from pycodealizer.entities.variables import VariableEntity, StarredEntity
from pycodealizer.parsers.base import EntityParser


class VariableParser(EntityParser):
    """Aggregates stats about variables."""

    def parse(self, node: ast.Name, module: Module, context: Context):
        """
        Add a variable to the statistics based on the type of context it
        is encountered in the source code.

        There are three possible context values:
            - `ast.Load` that denotes loading a variable's value, like in `print(a)`
            - `ast.Store` that denotes storing a value in a variable, like in `a = 1`
            - `ast.Del` that denotes deleting a variable, like in `del a`

        :param node: The node that represents a variable name to be added to the statistics.
        :param module: The python module where this variable is encountered.
        :param context: The context of the given node in the Abstract Syntax Tree.
        :return: ???
        """
        variable = VariableEntity(node)
        module.add_variable(variable)

        return variable


class StarredVariableParser(EntityParser):
    """Parse starred variable nodes."""

    def parse(self, node: ast.Starred, module: Module, context: Context):
        """Parse the value type of the ``ast.Starred`` node.

        Typically, the value is going to be a ``ast.Name`` node, but might be
        something else, although it's very improbable.

        Still, something like the following is valid Python code and will get executed ::

            def f1():
                return [1, 2, 3]

            def f2(*args):
                for arg in args:
                    print(arg)

            f2(*f1())

        The above example will yield ::

            1
            2
            3
        """
        starred_variable: StarredEntity = StarredEntity(node)
        context.stack_ast_node(starred_variable)

        parser = self.get_parser(node.value)
        entity = parser.parse(node.value, module, context)
        starred_variable.set_value_entity(entity)

        context.unstack_ast_node()
        module.add_starred_variable(starred_variable)

        return starred_variable


variable_parser = VariableParser()
starred_parser = StarredVariableParser()

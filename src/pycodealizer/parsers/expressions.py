import ast
from typing import Any

from pycodealizer.entities.common import Module, Context
from pycodealizer.entities.expressions import CallEntity, KeywordEntity, IfExpressionEntity
from pycodealizer.parsers.base import EntityParser


class CallParser(EntityParser):
    """Parses ``ast.Call`` nodes."""

    def parse(self, node: ast.Call, module: Module, context: Context):
        """Process a ``ast.Call`` node and extract relevant stats.

        A ``ast.Call`` node has the following fields:

            - ``func`` that represents the function, which will often be a ``ast.Name`` or ``ast.Attribute`` node
            - ``args`` that represents a list of the arguments passed by position
            - ``keywords`` that represents a list of keyword objects representing arguments passed by keyword
            - ``starargs`` holds a single node, for arguments passed as *args. This is removed in Python 3.5.
            - ``kwargs`` holds a single node, for arguments passed as **kwargs. This is removed in Python 3.5.

        :param node: The node that represents a call expression.
        :param module: The python module where this call is encountered.
        :param context: The context of the given node.
        :return: The CallEntity instance created from the given ``ast.Call`` node.
        """
        call: CallEntity = CallEntity(node, context)
        context.stack_ast_node(call)

        super().parse(node, module, context)

        context.unstack_ast_node()
        module.add_call(call)

        return call

    def parse_func(self, func: Any, module: Module, context: Context):
        """Parse the ``func`` node type that defines the call type.

        The ``func`` node can be either a ``ast.Name`` or ``ast.Attribute`` node.
        """
        call: CallEntity = context.current_ast_node

        parser = self.get_parser(func)
        func_entity = parser.parse(func, module, context)
        call.set_func(func_entity)

    def parse_args(self, arguments: list, module: Module, context: Context):
        """Process the "args" field of the ``ast.Call`` node.
        """
        call: CallEntity = context.current_ast_node

        for node in arguments:
            parser = self.get_parser(node)
            arg_entity = parser.parse(node, module, context)
            call.add_argument(arg_entity)

    def parse_keywords(self, keywords: list, module: Module, context: Context):
        """Process the "keywords" field of the ``ast.Call`` node.

        The list contains `ast.keyword` nodes that represent arguments passed by keyword.
        """
        call: CallEntity = context.current_ast_node

        for node in keywords:
            parser = self.get_parser(node.value)
            entity = parser.parse(node.value, module, context)
            keyword_entity = KeywordEntity(node.arg, entity)

            if keyword_entity.is_double_starred:
                call.set_starred_kwargs(keyword_entity)
            else:
                call.add_keyword(keyword_entity)

    def parse_starargs(self, stararg: Any, module: Module, context: Context):
        """Process the ``stararg`` field of the ``ast.Call`` node.

        This field was removed starting with Python 3.5. In versions of Python below 3.5,
        this field holds a single node to represent the arguments passed in as ``*args``
        to the function/method call.

        In case no starred arg is passed, this field will be ``None``.
        """
        call: CallEntity = context.current_ast_node

        if stararg:
            parser = self.get_parser(stararg)
            starred_entity = parser.parse(stararg, module, context)

            # Because prior to python 3.5 there was no ``ast.Starred`` node,
            # the returned entity should explicitly call ``mark_as_starred()``
            # method on itself, in order to mark it as starred. This happens
            # automatically in ``StarredEntity`` instances.
            starred_entity.mark_as_starred()

            call.set_starred_args(starred_entity)


class IfExpressionParser(EntityParser):
    """Parses ``ast.IfExp`` nodes."""

    def parse(self, node: Any, module: Module, context: Context):
        """Process a ``ast.IfExp`` node and extract relevant stats.

        A ``ast.IfExp`` node has the following fields:

            - ``test`` that represents the condition to be evaluated
            - ``body`` that represents the value to be assigned in case the condition evaluates to true
            - ``orelse`` that represents the value to be assigned in case the condition evaluates to false

        :param node: The node that represents an if expression.
        :param module: The python module where this expression is encountered.
        :param context: The context of the given node.
        :return: The ``pycodealizer.entities.IfExpressionEntity`` instance created from the given ``ast.IfExp`` node.
        """
        if_expression: IfExpressionEntity = IfExpressionEntity(node)
        context.stack_ast_node(if_expression)

        super().parse(node, module, context)

        context.unstack_ast_node()
        module.add_if_expression(if_expression)

        return if_expression

    def parse_field(self, node: Any, module: Module, context: Context, field: str):
        """Define generic behavior of parsing a field on a ``ast.IfExp`` node."""

        if_expression: IfExpressionEntity = context.current_ast_node

        parser = self.get_parser(node)
        node_entity = parser.parse(node, module, context)

        if_expression_setter = getattr(if_expression, f'set_{field}')
        if_expression_setter(node_entity)

    def parse_test(self, test: Any, module: Module, context: Context):
        self.parse_field(test, module, context, 'test')

    def parse_body(self, body: Any, module: Module, context: Context):
        self.parse_field(body, module, context, 'body')

    def parse_orelse(self, orelse: Any, module: Module, context: Context):
        self.parse_field(orelse, module, context, 'orelse')


call_parser = CallParser()
if_expression_parser = IfExpressionParser()
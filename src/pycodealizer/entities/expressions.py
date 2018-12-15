import ast
from typing import Any

from pycodealizer.constants import CALL, KEYWORD_ARGUMENT, STARRED_VAR, FUNCTION, VARIABLE, ATTRIBUTE, IF_EXPRESSION
from pycodealizer.entities.mixins import CommonMixin


class KeywordEntity(object):
    """Represent a keyword argument in a function call or function definition.

    The double starred variable definition (**kwargs, **vars) are also represented
    by this class, having the `arg` field set to None.
    """

    entity_type = KEYWORD_ARGUMENT

    def __init__(self, arg: Any, value: Any):
        self.arg = arg
        self.value = value
        self.value_type = value.entity_type
        self.is_double_starred = True if not arg else False

        self.propagate_state_to_child_nodes()

    def propagate_state_to_child_nodes(self):
        """Propagate the fact that this is a keyword argument to the value instance."""

        try:
            self.value.mark_as_participating_as_keyword_arg(in_function_call=True,
                                                            is_double_starred=self.is_double_starred)
        except AttributeError:
            print(f'||*************** {self.value.entity_type} has no "mark_as_participating_as_keyword_arg()" method.')

    def __repr__(self):
        if self.is_double_starred:
            return f'Kwarg: **{self.value.name}'
        return f'Kwarg: {self.arg}={self.value.name}'


class CallEntity(CommonMixin):
    """Represent a function or method call."""

    entity_type = CALL

    def __init__(self, node: ast.Call, context):
        self.line_nr = node.lineno
        self.func = None
        self.call_type = None
        self.arguments = list()
        self.argument_types = list()
        self.keyword_arguments = list()
        self.keyword_argument_types = list()
        self.args_var_name = None
        self.kwargs_var_name = None
        self.args_var_type = None
        self.kwargs_var_type = None

        self.ast_execution_context = context.current_ast_node
        self.execution_context = context.current_execution_context

        super().__init__()

    def set_func(self, entity: Any):
        """Set the name and type of the call."""

        self.func = entity
        self.call_type = FUNCTION if entity.entity_type == VARIABLE else ATTRIBUTE

    def add_argument(self, entity: Any):
        """Add an entity that was passed in as an argument to the function call."""

        # starting with python 3.5 onwards, the starred arguments (*args, *vars)
        # definition are represented by a `ast.Starred` node instead of being
        # present in the `starargs` field of the `ast.Call` node, that's why
        # the entity type should be checked here for its type
        if entity.entity_type == STARRED_VAR:
            self.set_starred_args(entity)
        else:
            self.arguments.append(entity)
            self.argument_types.append(entity.entity_type)

    def add_keyword(self, entity: KeywordEntity):
        """Add an entity that was passed in as a keyword argument to the function call."""

        self.keyword_arguments.append(entity)
        self.keyword_argument_types.append(entity.entity_type)

    def set_starred_args(self, entity: Any):
        """Add the name of the entity used when passing variable length args."""
        self.args_var_name = entity.name

        if entity.entity_type == STARRED_VAR:
            self.args_var_type = entity.value.entity_type
        else:
            self.args_var_type = entity.entity_type

    def set_starred_kwargs(self, entity: KeywordEntity):
        """Add the name of the entity used when passing variable length kwargs."""

        self.kwargs_var_name = entity.value.name
        self.kwargs_var_type = entity.value.entity_type

    @property
    def name(self):
        """The name of the entity."""
        return self.func.name


class IfExpressionEntity(object):
    """Represent an if expression of form ``a if b else c``."""

    entity_type = IF_EXPRESSION

    def __init__(self, node: ast.IfExp):
        self.line_nr = node.lineno
        self.test_entity = None
        self.test_entity_type = None
        self.body_entity = None
        self.body_entity_type = None
        self.orelse_entity = None
        self.orelse_entity_type = None

    def set_test(self, entity: Any):
        self.test_entity = entity
        self.test_entity_type = entity.entity_type

        entity.mark_as_part_of_if_test_condition(inside_if_expression=True)

    def set_body(self, entity: Any):
        self.body_entity = entity
        self.body_entity_type = entity.entity_type

        entity.mark_as_part_of_if_body(inside_if_expression=True)

    def set_orelse(self, entity: Any):
        self.orelse_entity = entity
        self.orelse_entity_type = entity.entity_type

        entity.mark_as_part_of_if_orelse(inside_if_expression=True)

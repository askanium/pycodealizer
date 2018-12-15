import ast

import pytest
from pytest_lazyfixture import lazy_fixture

from pycodealizer.constants import NUMBER
from pycodealizer.entities.common import Module, Context
from pycodealizer.entities.variables import VariableEntity


def test_context_initialization(module_entity: Module):
    context = Context(module_entity)

    assert len(context.execution_context) == 1 and context.execution_context[0] == module_entity
    assert len(context.ast_context) == 1 and context.ast_context[0] == module_entity


def test_context_stack_execution_context(variable_load_entity: VariableEntity, context: Context):
    context.stack_execution_context(variable_load_entity)

    assert len(context.execution_context) == 2 and context.execution_context[-1] == variable_load_entity


def test_context_unstack_execution_context(variable_load_entity: VariableEntity, context: Context):
    context.stack_execution_context(variable_load_entity)
    context.unstack_execution_context()

    assert len(context.execution_context) == 1


def test_context_stack_ast_node(ast_var_node: ast.Name, context: Context):
    context.stack_ast_node(ast_var_node)

    assert len(context.ast_context) == 2 and context.ast_context[-1] == ast_var_node


def test_context_unstack_ast_node(ast_var_node: ast.Name, context: Context):
    context.stack_ast_node(ast_var_node)
    context.unstack_ast_node()

    assert len(context.ast_context) == 1


def test_context_current_execution_context_prop(variable_load_entity: VariableEntity, context: Context):
    context.stack_execution_context(variable_load_entity)

    assert context.current_execution_context == variable_load_entity


def test_context_current_ast_node_prop(ast_var_node: ast.Name, context: Context):
    context.stack_ast_node(ast_var_node)

    assert context.current_ast_node == ast_var_node


@pytest.mark.parametrize('entity,method_name,attribute', [
    (lazy_fixture('variable_load_entity'), 'add_variable', 'variables'),
    (lazy_fixture('starred_entity'), 'add_starred_variable', 'starred_variables'),
    (lazy_fixture('number_int_entity'), 'add_number', 'numbers'),
    (lazy_fixture('string_entity'), 'add_string', 'strings'),
    (lazy_fixture('tuple_entity'), 'add_tuple', 'tuples'),
    (lazy_fixture('list_entity'), 'add_list', 'lists'),
    (lazy_fixture('set_entity'), 'add_set', 'sets'),
    (lazy_fixture('assignment_entity'), 'add_assignment', 'assignments'),
    (lazy_fixture('call_entity'), 'add_call', 'calls'),
    (lazy_fixture('if_expression_entity'), 'add_if_expression', 'if_expressions'),
])
def test_module_add_method(entity, method_name, attribute, module_entity: Module, context: Context):
    method = getattr(module_entity, method_name)
    method(entity)

    assert len(getattr(module_entity, attribute)) == 1 and getattr(module_entity, attribute)[0] == entity
    assert getattr(module_entity, 'line_numbers')[entity.line_nr][0] == entity
    assert getattr(module_entity, 'type_line_numbers')[entity.line_nr][0] == entity.entity_type if entity.entity_type != NUMBER else entity.value_type

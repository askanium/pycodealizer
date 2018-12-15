import ast
import pytest

from pycodealizer.constants import STARRED_VAR
from pycodealizer.entities.literals import TupleEntity, ListEntity
from pycodealizer.entities.statements import AssignmentEntity
from pycodealizer.entities.variables import VariableEntity, StarredEntity


def test_variable_initialization(ast_var_node: ast.Name):
    variable = VariableEntity(ast_var_node)

    assert variable.line_nr == ast_var_node.lineno
    assert variable.name == ast_var_node.id
    assert variable.context == 'Load'
    assert variable.used_in_unpacking_assignment is False


def test_variable_representation(variable_load_entity: VariableEntity):
    assert repr(variable_load_entity) == 'Variable: a'


@pytest.mark.parametrize('in_tuple,in_list', [
    (True, False),
    (False, True)
])
def test_variable_mark_as_participating_in_unpacking(variable_load_entity: VariableEntity, in_tuple: bool, in_list: bool):
    variable_load_entity.mark_as_participating_in_unpacking(in_tuple=in_tuple, in_list=in_list)

    assert variable_load_entity.used_in_unpacking_assignment is True
    assert variable_load_entity.used_in_tuple == in_tuple
    assert variable_load_entity.used_in_list == in_list


@pytest.mark.parametrize('is_double_starred', [True, False])
def test_variable_mark_as_participating_as_keyword_arg(variable_load_entity: VariableEntity, is_double_starred: bool):
    variable_load_entity.mark_as_participating_as_keyword_arg(True, False, is_double_starred)

    assert variable_load_entity.used_in_function_call is True
    assert variable_load_entity.used_in_function_definition is False
    assert variable_load_entity.is_double_starred == is_double_starred


def test_starred_entity_initialization(ast_starred_node: ast.Starred):
    starred_entity = StarredEntity(ast_starred_node)

    assert starred_entity.entity_type == STARRED_VAR
    assert starred_entity.value is None
    assert starred_entity.context == 'Load'


def test_starred_entity_set_value(mocker, ast_starred_node, ast_var_node):
    variable = VariableEntity(ast_var_node)
    starred_entity = StarredEntity(ast_starred_node)

    mocker.spy(variable, 'mark_as_starred')

    starred_entity.set_value_entity(variable)

    assert starred_entity.value == variable
    assert variable.mark_as_starred.call_count == 1


def test_starred_entity_name_property(starred_entity):
    assert starred_entity.name == 'a'

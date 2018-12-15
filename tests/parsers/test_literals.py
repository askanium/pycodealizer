import ast

import pytest
from pytest_lazyfixture import lazy_fixture

from pycodealizer.entities.common import Module, Context
from pycodealizer.entities.literals import SetEntity, TupleEntity, ListEntity, NumberEntity, StringEntity
from pycodealizer.parsers.literals import SetParser, TupleParser, ListParser, BaseSequenceParser, NumberParser, \
    StringParser


def test_base_sequence_parser_parse(mocker, module_entity: Module, context: Context, ast_set_node: ast.Set):
    parser = BaseSequenceParser()

    mocker.spy(context, 'stack_ast_node')
    mocker.spy(context, 'unstack_ast_node')
    entity = mocker.MagicMock()
    parser.add_entity_to_module = mocker.MagicMock()
    parser.create_new_entity = mocker.MagicMock()
    parser.create_new_entity.return_value = entity

    result = parser.parse(ast_set_node, module_entity, context)

    assert context.stack_ast_node.call_count == 1
    assert context.unstack_ast_node.call_count == 1
    assert entity == result
    parser.create_new_entity.assert_called_once_with(ast_set_node)
    parser.add_entity_to_module.assert_called_once_with(entity, module_entity, context)


def test_base_sequence_parser_parses_node_elements(mocker, module_entity: Module, context: Context, ast_list_node: ast.List):
    parser = BaseSequenceParser()

    parser.create_new_entity = mocker.MagicMock()
    parser.add_entity_to_module = mocker.MagicMock()
    parser.get_parser = mocker.MagicMock()

    entity_mock = mocker.MagicMock()
    parser.create_new_entity.return_value = entity_mock

    child_parser = mocker.MagicMock()
    parser.get_parser.return_value = child_parser

    child_entity_mock = mocker.MagicMock()
    child_parser.parse.return_value == child_entity_mock

    parser.parse(ast_list_node, module_entity, context)

    assert parser.get_parser.call_count == 3
    assert child_parser.parse.call_count == 3
    assert entity_mock.add_element.has_calls([mocker.call(child_entity_mock)])


@pytest.mark.parametrize('ast_node,parser_class,entity_class', [
    (lazy_fixture('ast_set_node'), SetParser, SetEntity),
    (lazy_fixture('ast_tuple_node'), TupleParser, TupleEntity),
    (lazy_fixture('ast_list_node'), ListParser, ListEntity),
])
def test_sequence_parser_create_new_entity(ast_node, parser_class, entity_class):
    parser = parser_class()

    entity = parser.create_new_entity(ast_node)

    assert isinstance(entity, entity_class)
    assert entity.nr_of_elements == 0  # upon creation, the entity should have no elements


@pytest.mark.parametrize('entity,parser_class,method', [
    (lazy_fixture('set_entity'), SetParser, 'add_set'),
    (lazy_fixture('tuple_entity'), TupleParser, 'add_tuple'),
    (lazy_fixture('list_entity'), ListParser, 'add_list'),
])
def test_sequence_parser_add_entity_to_module(mocker, module_entity: Module, context: Context, entity, parser_class, method):
    mocker.spy(module_entity, method)

    parser = parser_class()
    parser.add_entity_to_module(entity, module_entity)

    assert getattr(module_entity, method).call_count == 1


@pytest.mark.parametrize('ast_node,parser_class,entity_class,method', [
    (lazy_fixture('ast_num_node'), NumberParser, NumberEntity, 'add_number'),
    (lazy_fixture('ast_str_node'), StringParser, StringEntity, 'add_string'),
])
def test_primitives_parser_parse(mocker, module_entity: Module, context: Context, ast_node, parser_class, entity_class, method):
    parser = parser_class()

    mocker.spy(module_entity, method)

    entity = parser.parse(ast_node, module_entity, context)

    assert getattr(module_entity, method).call_count == 1
    assert isinstance(entity, entity_class)

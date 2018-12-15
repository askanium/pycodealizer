import pytest

from pycodealizer.entities.common import Module, Context
from pycodealizer.entities.expressions import CallEntity, IfExpressionEntity
from pycodealizer.parsers.expressions import CallParser, IfExpressionParser


def test_call_parser_parse(mocker, module_entity: Module, context: Context, ast_call_node):
    parser = CallParser()

    mocker.spy(context, 'stack_ast_node')
    mocker.spy(context, 'unstack_ast_node')
    mocker.spy(module_entity, 'add_call')

    for field in ast_call_node._fields:
        mocker.spy(parser, f'parse_{field}')

    result = parser.parse(ast_call_node, module_entity, context)

    assert context.stack_ast_node.call_count == 1
    assert context.unstack_ast_node.call_count == 1
    assert module_entity.add_call.call_count == 1
    assert isinstance(result, CallEntity)

    for field in ast_call_node._fields:
        assert getattr(parser, f'parse_{field}').call_count == 1


def test_call_parser_parse_func(mocker, ast_call_name_node, call_name_entity, module_entity: Module):
    parser = mocker.MagicMock(spec=CallParser)
    parser.parse_func = CallParser.parse_func

    call_entity = mocker.MagicMock()
    context = mocker.MagicMock()
    type(context).current_ast_node = mocker.PropertyMock(return_value=call_entity)

    func_parser = mocker.MagicMock()
    parser.get_parser.return_value = func_parser
    func_parser.parse.return_value = call_name_entity

    parser.parse_func(parser, ast_call_name_node, module_entity, context)

    parser.get_parser.assert_called_once_with(ast_call_name_node)
    func_parser.parse.assert_called_once_with(ast_call_name_node, module_entity, context)
    call_entity.set_func.assert_called_once_with(call_name_entity)


def test_call_parser_parse_args(mocker, module_entity: Module):
    parser = mocker.MagicMock(spec=CallParser)
    parser.parse_args = CallParser.parse_args

    call_entity = mocker.MagicMock()
    context = mocker.MagicMock()
    type(context).current_ast_node = mocker.PropertyMock(return_value=call_entity)

    args = [1, 2, 3]  # random data, needed to test function calls only
    arg_entities = [4, 5, 6]  # random data, needed to test function calls only
    arg_parser = mocker.MagicMock()
    parser.get_parser.return_value = arg_parser
    arg_parser.parse.side_effect = arg_entities

    parser.parse_args(parser, args, module_entity, context)

    assert parser.get_parser.call_args_list == [((1,),), ((2,),), ((3,),)]
    assert arg_parser.parse.call_args_list == [((1, module_entity, context),), ((2, module_entity, context),), ((3, module_entity, context),)]
    assert call_entity.add_argument.call_args_list == [((4,),), ((5,),), ((6,),)]


def test_if_expression_parser_parse(mocker, ast_ifexp_node, module_entity: Module, context: Context):
    parser = mocker.MagicMock(spec=IfExpressionParser)
    parser.parse = IfExpressionParser.parse

    mocker.spy(context, 'stack_ast_node')
    mocker.spy(context, 'unstack_ast_node')
    mocker.spy(module_entity, 'add_if_expression')

    for field in ast_ifexp_node._fields:
        mocker.spy(parser, f'parse_{field}')

    result = parser.parse(parser, ast_ifexp_node, module_entity, context)

    assert context.stack_ast_node.call_count == 1
    assert context.unstack_ast_node.call_count == 1
    assert module_entity.add_if_expression.call_count == 1
    assert isinstance(result, IfExpressionEntity)

    for field in ast_ifexp_node._fields:
        assert getattr(parser, f'parse_{field}').call_count == 1


@pytest.mark.parametrize('field', ['test', 'body', 'orelse'])
def test_if_expression_parser_parse_field(mocker, module_entity: Module, field: str):
    parser = mocker.MagicMock(spec=IfExpressionParser)
    parser.parse_field = IfExpressionParser.parse_field

    if_expression_entity = mocker.MagicMock()
    context = mocker.MagicMock()
    type(context).current_ast_node = mocker.PropertyMock(return_value=if_expression_entity)

    field_parser = mocker.MagicMock()
    parser.get_parser.return_value = field_parser
    node_entity = mocker.MagicMock()
    field_parser.parse.return_value = node_entity

    ast_node = mocker.MagicMock()

    parser.parse_field(parser, ast_node, module_entity, context, field)

    parser.get_parser.assert_called_once_with(ast_node)
    field_parser.parse.assert_called_once_with(ast_node, module_entity, context)
    getattr(if_expression_entity, f'set_{field}').assert_called_once_with(node_entity)


@pytest.mark.parametrize('field', ['test', 'body', 'orelse'])
def test_if_expression_parser_parse_test(mocker, field, module_entity: Module, context: Context):
    parser = IfExpressionParser()

    mocker.spy(parser, 'parse_field')
    parser.parse_field = mocker.MagicMock()
    ast_node = mocker.MagicMock()

    field_parser = getattr(parser, f'parse_{field}')
    field_parser(ast_node, module_entity, context)

    parser.parse_field.assert_called_once_with(ast_node, module_entity, context, field)

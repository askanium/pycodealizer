from pycodealizer.entities.common import Module, Context
from pycodealizer.entities.variables import VariableEntity, StarredEntity
from pycodealizer.parsers.variables import VariableParser, StarredVariableParser


def test_variable_parser_parse(mocker, module_entity: Module, context: Context, ast_var_node):
    parser = VariableParser()

    mocker.spy(module_entity, 'add_variable')

    result = parser.parse(ast_var_node, module_entity, context)

    assert module_entity.add_variable.call_count == 1
    assert isinstance(result, VariableEntity)


def test_starred_variable_parser_parse(mocker, module_entity: Module, context: Context, ast_starred_node):
    parser = StarredVariableParser()

    mocker.spy(context, 'stack_ast_node')
    mocker.spy(context, 'unstack_ast_node')
    mocker.spy(module_entity, 'add_starred_variable')

    result = parser.parse(ast_starred_node, module_entity, context)

    assert context.stack_ast_node.call_count == 1
    assert context.unstack_ast_node.call_count == 1
    assert module_entity.add_starred_variable.call_count == 1
    assert isinstance(result, StarredEntity)

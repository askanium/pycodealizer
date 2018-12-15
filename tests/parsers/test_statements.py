from pycodealizer.entities.common import Module, Context
from pycodealizer.entities.statements import AssignmentEntity
from pycodealizer.parsers.statements import AssignmentParser


def test_assignment_parser_parse(mocker, module_entity: Module, context: Context, ast_assign_node):
    parser = AssignmentParser()

    mocker.spy(context, 'stack_ast_node')
    mocker.spy(context, 'unstack_ast_node')
    mocker.spy(module_entity, 'add_assignment')

    for field in ast_assign_node._fields:
        mocker.spy(parser, f'parse_{field}')

    result = parser.parse(ast_assign_node, module_entity, context)

    assert context.stack_ast_node.call_count == 1
    assert context.unstack_ast_node.call_count == 1
    assert module_entity.add_assignment.call_count == 1
    assert isinstance(result, AssignmentEntity)

    for field in ast_assign_node._fields:
        assert getattr(parser, f'parse_{field}').call_count == 1


def test_assignment_parser_parse_targets(mocker, module_entity: Module):
    parser = mocker.MagicMock(spec=AssignmentParser)
    parser.parse_targets = AssignmentParser.parse_targets

    assignment_entity = mocker.MagicMock()
    context = mocker.MagicMock()
    type(context).current_ast_node = mocker.PropertyMock(return_value=assignment_entity)

    targets = [1, 2, 3]  # random data, needed to test function calls only
    target_entities = [4, 5, 6]  # random data, needed to test function calls only
    target_parser = mocker.MagicMock()
    parser.get_parser.return_value = target_parser
    target_parser.parse.side_effect = target_entities

    parser.parse_targets(parser, targets, module_entity, context)

    assert parser.get_parser.call_args_list == [((1,),), ((2,),), ((3,),)]
    assert target_parser.parse.call_args_list == [((1, module_entity, context),), ((2, module_entity, context),), ((3, module_entity, context),)]
    assert assignment_entity.add_target.call_args_list == [((4,),), ((5,),), ((6,),)]


def test_assignment_parser_parse_value(mocker, ast_assign_node, assignment_entity, module_entity: Module):
    parser = mocker.MagicMock(spec=AssignmentParser)
    parser.parse_value = AssignmentParser.parse_value

    assignment_entity = mocker.MagicMock()
    context = mocker.MagicMock()
    type(context).current_ast_node = mocker.PropertyMock(return_value=assignment_entity)

    value_parser = mocker.MagicMock()
    parser.get_parser.return_value = value_parser
    value_parser.parse.return_value = assignment_entity

    parser.parse_value(parser, ast_assign_node, module_entity, context)

    parser.get_parser.assert_called_once_with(ast_assign_node)
    value_parser.parse.assert_called_once_with(ast_assign_node, module_entity, context)
    assignment_entity.add_value.assert_called_once_with(assignment_entity)

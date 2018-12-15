import ast

from pycodealizer.constants import KEYWORD_ARGUMENT, VARIABLE, FUNCTION
from pycodealizer.entities.common import Context
from pycodealizer.entities.expressions import KeywordEntity, CallEntity, IfExpressionEntity
from pycodealizer.entities.variables import StarredEntity, VariableEntity


def test_keyword_entity_initialization_with_non_double_starred_var(keyword_argument_var_entity: KeywordEntity):
    assert keyword_argument_var_entity.entity_type == KEYWORD_ARGUMENT
    assert keyword_argument_var_entity.value_type == VARIABLE
    assert keyword_argument_var_entity.is_double_starred is False


def test_keyword_entity_initialization_with_double_starred_var(keyword_argument_double_starred_entity: KeywordEntity):
    assert keyword_argument_double_starred_entity.entity_type == KEYWORD_ARGUMENT
    assert keyword_argument_double_starred_entity.value_type == VARIABLE
    assert keyword_argument_double_starred_entity.is_double_starred is True


def test_keyword_entity_initialization_propagates_state_to_children(mocker):
    variable = mocker.MagicMock()
    keyword = KeywordEntity(arg='test', value=variable)
    keyword.value.mark_as_participating_as_keyword_arg.assert_called_once_with(in_function_call=True,
                                                                               is_double_starred=False)


def test_keyword_entity_has_correct_representation(keyword_argument_var_entity):
    assert repr(keyword_argument_var_entity) == 'Kwarg: ka=a'


def test_double_starred_keyword_entity_has_correct_representation(keyword_argument_double_starred_entity):
    assert repr(keyword_argument_double_starred_entity) == 'Kwarg: **a'


def test_call_entity_initialization(ast_call_node: ast.Call, context: Context):
    call_entity = CallEntity(ast_call_node, context)
    assert call_entity.line_nr == 1
    assert call_entity.func is None
    assert call_entity.call_type is None
    assert len(call_entity.arguments) == 0
    assert len(call_entity.argument_types) == 0
    assert len(call_entity.keyword_arguments) == 0
    assert len(call_entity.keyword_argument_types) == 0
    assert call_entity.args_var_name is None
    assert call_entity.kwargs_var_name is None
    assert call_entity.args_var_type is None
    assert call_entity.kwargs_var_type is None
    assert call_entity.ast_execution_context == context.current_ast_node
    assert call_entity.execution_context == context.current_execution_context


def test_call_entity_set_func(call_entity: CallEntity, call_name_entity: VariableEntity):
    assert call_entity.func is None
    assert call_entity.call_type is None

    call_entity.set_func(call_name_entity)

    assert call_entity.func == call_name_entity
    assert call_entity.call_type == FUNCTION


def test_call_name_property(call_entity: CallEntity, call_name_entity: VariableEntity):
    call_entity.set_func(call_name_entity)

    assert call_entity.name == 'fn'


# TODO add test case for method call (after implementing AttributeEntity class)


def test_call_entity_add_argument(mocker, call_entity: CallEntity, variable_load_entity: VariableEntity):
    assert len(call_entity.arguments) == 0
    assert len(call_entity.argument_types) == 0

    mocker.spy(call_entity, 'set_starred_args')

    call_entity.add_argument(variable_load_entity)

    assert len(call_entity.arguments) == 1
    assert call_entity.argument_types[0] == VARIABLE
    assert call_entity.args_var_name is None
    assert call_entity.set_starred_args.call_count == 0


def test_call_entity_add_starred_argument(mocker, call_entity: CallEntity, starred_entity):
    assert len(call_entity.arguments) == 0
    assert len(call_entity.argument_types) == 0
    assert call_entity.args_var_name is None

    mocker.spy(call_entity, 'set_starred_args')

    call_entity.add_argument(starred_entity)

    assert len(call_entity.arguments) == 0
    assert len(call_entity.argument_types) == 0
    assert call_entity.args_var_name == starred_entity.value.name
    assert call_entity.args_var_type == starred_entity.value.entity_type
    assert call_entity.set_starred_args.call_count == 1


def test_call_entity_add_keyword(call_entity: CallEntity, keyword_argument_var_entity: KeywordEntity):
    assert len(call_entity.keyword_arguments) == 0
    assert len(call_entity.keyword_argument_types) == 0

    call_entity.add_keyword(keyword_argument_var_entity)

    assert len(call_entity.keyword_arguments) == 1 \
           and call_entity.keyword_arguments[0] == keyword_argument_var_entity
    assert len(call_entity.keyword_argument_types) == 1 \
           and call_entity.keyword_argument_types[0] == keyword_argument_var_entity.entity_type
    assert call_entity.kwargs_var_name is None


def test_call_entity_add_double_starred_keyword_argument(call_entity: CallEntity, keyword_argument_double_starred_entity: KeywordEntity):
    assert len(call_entity.keyword_arguments) == 0
    assert len(call_entity.keyword_argument_types) == 0
    assert call_entity.kwargs_var_name is None

    call_entity.set_starred_kwargs(keyword_argument_double_starred_entity)

    assert len(call_entity.keyword_arguments) == 0
    assert len(call_entity.keyword_argument_types) == 0
    assert call_entity.kwargs_var_name == keyword_argument_double_starred_entity.value.name
    assert call_entity.kwargs_var_type == keyword_argument_double_starred_entity.value.entity_type


def test_if_expression_initializatiokn(if_expression_entity: IfExpressionEntity):
    assert if_expression_entity.line_nr == 1
    assert if_expression_entity.test_entity is None
    assert if_expression_entity.test_entity_type is None
    assert if_expression_entity.body_entity is None
    assert if_expression_entity.body_entity_type is None
    assert if_expression_entity.orelse_entity is None
    assert if_expression_entity.orelse_entity_type is None


def test_if_expression_set_test(mocker, if_expression_entity: IfExpressionEntity, evaluatable_entity):
    mocker.spy(evaluatable_entity, 'mark_as_part_of_if_test_condition')
    assert if_expression_entity.test_entity is None
    assert if_expression_entity.test_entity_type is None

    if_expression_entity.set_test(evaluatable_entity)

    assert if_expression_entity.test_entity == evaluatable_entity
    assert if_expression_entity.test_entity_type == evaluatable_entity.entity_type
    assert evaluatable_entity.mark_as_part_of_if_test_condition.call_count == 1
    assert evaluatable_entity.is_part_of_if_test_condition is True
    assert evaluatable_entity.is_part_of_an_if_expression is True


def test_if_expression_set_body(mocker, if_expression_entity: IfExpressionEntity, common_entity):
    mocker.spy(common_entity, 'mark_as_part_of_if_body')
    assert if_expression_entity.body_entity is None
    assert if_expression_entity.body_entity_type is None

    if_expression_entity.set_body(common_entity)

    assert if_expression_entity.body_entity == common_entity
    assert if_expression_entity.body_entity_type == common_entity.entity_type
    assert common_entity.mark_as_part_of_if_body.call_count == 1
    assert common_entity.is_part_of_if_body is True
    assert common_entity.is_part_of_an_if_expression is True


def test_if_expression_set_orelse(mocker, if_expression_entity: IfExpressionEntity, common_entity):
    mocker.spy(common_entity, 'mark_as_part_of_if_orelse')
    assert if_expression_entity.orelse_entity is None
    assert if_expression_entity.orelse_entity_type is None

    if_expression_entity.set_orelse(common_entity)

    assert if_expression_entity.orelse_entity == common_entity
    assert if_expression_entity.orelse_entity_type == common_entity.entity_type
    assert common_entity.mark_as_part_of_if_orelse.call_count == 1
    assert common_entity.is_part_of_if_orelse is True
    assert common_entity.is_part_of_an_if_expression is True

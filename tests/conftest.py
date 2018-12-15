import ast

import pytest
from pytest_lazyfixture import lazy_fixture

from pycodealizer.entities.common import Module, Context
from pycodealizer.entities.expressions import KeywordEntity, CallEntity, IfExpressionEntity
from pycodealizer.entities.literals import NumberEntity, TupleEntity, ListEntity, StringEntity, SetEntity
from pycodealizer.entities.statements import AssignmentEntity
from pycodealizer.entities.variables import VariableEntity, StarredEntity


ast_name_load = ast.parse('a').body[0].value
ast_name_store = ast.Name(id='a', ctx=ast.Store(), lineno=1, col_offset=0)
ast_str = ast.parse('"test"').body[0].value
ast_int_num = ast.parse('2').body[0].value
ast_float_num = ast.parse('2.0').body[0].value
ast_complex_num = ast.parse('2j').body[0].value
ast_call = ast.parse('fn()').body[0].value
ast_call_name = ast.parse('fn').body[0].value
ast_starred_var = ast.parse('*a').body[0].value
ast_assign = ast.parse('a = 2').body[0]
ast_tuple_load = ast.parse('(1, 2, 3)').body[0].value
ast_list_load = ast.parse('[1, 2, 3]').body[0].value
ast_set = ast.parse('{1, 2, 3}').body[0].value
ast_ifexp = ast.parse('1 if True else a').body[0].value


@pytest.fixture
def variable_load_entity():
    return VariableEntity(ast_name_load)


@pytest.fixture
def variable_store_entity():
    return VariableEntity(ast_name_store)


@pytest.fixture
def keyword_argument_var_entity():
    return KeywordEntity(arg='ka', value=VariableEntity(ast_name_load))


@pytest.fixture
def keyword_argument_double_starred_entity():
    return KeywordEntity(arg=None, value=VariableEntity(ast_name_load))


@pytest.fixture
def keyword_argument_num_entity():
    return KeywordEntity(arg='ka', value=VariableEntity(ast_name_load))


@pytest.fixture
def assignment_entity():
    return AssignmentEntity(ast_assign)


@pytest.fixture
def call_name_entity():
    return VariableEntity(ast_call_name)


@pytest.fixture
def call_entity():
    return CallEntity(ast_call, Context(Module('test')))


@pytest.fixture
def starred_entity():
    starred_entity = StarredEntity(ast_starred_var)
    starred_entity.set_value_entity(VariableEntity(ast_name_load))
    return starred_entity


@pytest.fixture
def number_int_entity():
    return NumberEntity(ast_int_num)


@pytest.fixture
def string_entity():
    return StringEntity(ast_str)


@pytest.fixture
def number_float_entity():
    return NumberEntity(ast_float_num)


@pytest.fixture
def number_complex_entity():
    return NumberEntity(ast_complex_num)


@pytest.fixture
def tuple_entity():
    return TupleEntity(ast_tuple_load)


@pytest.fixture
def list_entity():
    return ListEntity(ast_list_load)


@pytest.fixture
def set_entity():
    return SetEntity(ast_set)


@pytest.fixture
def if_expression_entity():
    return IfExpressionEntity(ast_ifexp)


@pytest.fixture
def module_entity():
    return Module('test')


@pytest.fixture
def context():
    return Context(Module('test'))


@pytest.fixture(params=[
    lazy_fixture('number_int_entity'),
    lazy_fixture('string_entity'),
    lazy_fixture('tuple_entity'),
    lazy_fixture('list_entity'),
    lazy_fixture('set_entity'),
])
def literal_entity(request):
    return request.param


@pytest.fixture(params=[
    lazy_fixture('variable_load_entity'),
    lazy_fixture('number_int_entity'),
    lazy_fixture('string_entity'),
    lazy_fixture('tuple_entity'),
    lazy_fixture('list_entity'),
    lazy_fixture('set_entity'),
    lazy_fixture('call_entity'),
])
def common_entity(request):
    return request.param


@pytest.fixture(params=[
    lazy_fixture('variable_load_entity'),
    lazy_fixture('call_entity')
])
def evaluatable_entity(request):
    return request.param


@pytest.fixture
def ast_var_node():
    return ast_name_load


@pytest.fixture
def ast_set_node():
    return ast_set


@pytest.fixture
def ast_tuple_node():
    return ast_tuple_load


@pytest.fixture
def ast_list_node():
    return ast_list_load


@pytest.fixture
def ast_num_node():
    return ast_int_num


@pytest.fixture
def ast_str_node():
    return ast_str


@pytest.fixture
def ast_call_node():
    return ast_call


@pytest.fixture
def ast_call_name_node():
    return ast_call_name


@pytest.fixture
def ast_ifexp_node():
    return ast_ifexp


@pytest.fixture
def ast_assign_node():
    return ast_assign


@pytest.fixture
def ast_starred_node():
    return ast_starred_var


@pytest.fixture(params=[
    lazy_fixture('ast_var_node'),
    lazy_fixture('ast_call_node')
])
def ast_evaluabable_node(request):
    return request.param


@pytest.fixture(params=[
    lazy_fixture('ast_var_node'),
    lazy_fixture('ast_num_node'),
    lazy_fixture('ast_str_node'),
    lazy_fixture('ast_tuple_node'),
    lazy_fixture('ast_list_node'),
    lazy_fixture('ast_set_node'),
    lazy_fixture('ast_call_node'),
])
def ast_common_node(request):
    return request.param

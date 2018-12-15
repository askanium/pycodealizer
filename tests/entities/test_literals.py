import pytest

from pycodealizer.constants import NUMBER, TUPLE, UsageContexts, LIST, STRING, SET
from pycodealizer.entities.literals import NumberEntity, TupleEntity, ListEntity, StringEntity, SetEntity


def test_string_entity_initialization(string_entity: StringEntity):
    assert string_entity.entity_type == STRING
    assert string_entity.value == 'test'
    assert string_entity.value_length == 4


def test_string_entity_representation(string_entity: StringEntity):
    assert repr(string_entity) == 'test (4 chars)'


def test_number_integer_entity_initialization(number_int_entity: NumberEntity):
    assert number_int_entity.entity_type == NUMBER
    assert number_int_entity.value == number_int_entity.value
    assert number_int_entity.value_type == 'int'


def test_number_float_entity_initialization(number_float_entity: NumberEntity):
    assert number_float_entity.entity_type == NUMBER
    assert number_float_entity.value == number_float_entity.value
    assert number_float_entity.value_type == 'float'


def test_number_complex_entity_initialization(number_complex_entity: NumberEntity):
    assert number_complex_entity.entity_type == NUMBER
    assert number_complex_entity.value == number_complex_entity.value
    assert number_complex_entity.value_type == 'complex'


def test_number_entity_has_correct_representation(number_float_entity: NumberEntity):
    assert repr(number_float_entity) == 'float: 2.0'


def test_tuple_entity_initialization(tuple_entity):
    assert tuple_entity.entity_type == TUPLE
    assert tuple_entity.context == UsageContexts.LOAD.value
    assert len(tuple_entity.elements) == 0


def test_tuple_entity_add_element(mocker, tuple_entity, literal_entity):
    assert len(tuple_entity.elements) == 0

    mocker.spy(literal_entity, 'mark_as_used_in_tuple')

    tuple_entity.add_element(literal_entity)

    assert len(tuple_entity.elements) == 1 and tuple_entity.elements[0] == literal_entity
    assert literal_entity.mark_as_used_in_tuple.call_count == 1


def test_tuple_entity_mark_as_used_for_unpacking(mocker, tuple_entity, variable_load_entity):
    tuple_entity.add_element(variable_load_entity)
    mocker.spy(variable_load_entity, 'mark_as_participating_in_unpacking')

    assert len(tuple_entity.elements) == 1

    tuple_entity.used_for_unpacking()

    args, kwargs = variable_load_entity.mark_as_participating_in_unpacking.call_args

    assert variable_load_entity.mark_as_participating_in_unpacking.call_count == 1
    assert args == ()
    assert kwargs == {'in_tuple': True}


def test_tuple_nr_of_elements_property(tuple_entity, number_float_entity: NumberEntity):
    assert tuple_entity.nr_of_elements == 0

    tuple_entity.add_element(number_float_entity)

    assert tuple_entity.nr_of_elements == 1


def test_list_entity_initialization(list_entity: ListEntity):
    assert list_entity.entity_type == LIST
    assert list_entity.context == UsageContexts.LOAD.value
    assert len(list_entity.elements) == 0


def test_list_entity_add_element(mocker, list_entity, literal_entity):
    assert len(list_entity.elements) == 0

    mocker.spy(literal_entity, 'mark_as_used_in_list')

    list_entity.add_element(literal_entity)

    assert len(list_entity.elements) == 1 and list_entity.elements[0] == literal_entity
    assert literal_entity.mark_as_used_in_list.call_count == 1


def test_list_entity_mark_as_used_for_unpacking(mocker, list_entity, variable_load_entity):
    list_entity.add_element(variable_load_entity)
    mocker.spy(variable_load_entity, 'mark_as_participating_in_unpacking')

    assert len(list_entity.elements) == 1

    list_entity.used_for_unpacking()

    args, kwargs = variable_load_entity.mark_as_participating_in_unpacking.call_args

    assert variable_load_entity.mark_as_participating_in_unpacking.call_count == 1
    assert args == ()
    assert kwargs == {'in_list': True}


def test_list_nr_of_elements_property(list_entity, number_float_entity: NumberEntity):
    assert list_entity.nr_of_elements == 0

    list_entity.add_element(number_float_entity)

    assert list_entity.nr_of_elements == 1


def test_set_entity_initialization(set_entity: SetEntity):
    assert set_entity.entity_type == SET
    assert len(set_entity.elements) == 0


def test_set_entity_add_element(mocker, set_entity: SetEntity, common_entity):
    mocker.spy(common_entity, 'mark_as_used_in_set')
    assert len(set_entity.elements) == 0

    set_entity.add_element(common_entity)

    assert len(set_entity.elements) == 1 and set_entity.elements[0] == common_entity
    assert common_entity.mark_as_used_in_set.call_count == 1


def test_set_entity_nr_of_elements_property(set_entity: SetEntity, number_float_entity: NumberEntity):
    assert set_entity.nr_of_elements == 0

    set_entity.add_element(number_float_entity)

    assert set_entity.nr_of_elements == 1

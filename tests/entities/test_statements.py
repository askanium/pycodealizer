from pycodealizer.entities.literals import TupleEntity, ListEntity
from pycodealizer.entities.statements import AssignmentEntity
from pycodealizer.entities.variables import VariableEntity


def test_assignment_add_value(mocker, assignment_entity: AssignmentEntity, common_entity):
    mocker.spy(common_entity, 'mark_as_assignment_value')

    assert assignment_entity.value_initialized is False

    assignment_entity.add_value(common_entity)

    assert assignment_entity.value == common_entity
    assert assignment_entity.value_type == common_entity.entity_type
    assert common_entity.mark_as_assignment_value.call_count == 1
    assert assignment_entity.value_initialized is True


def test_assignment_add_target(mocker, assignment_entity: AssignmentEntity, variable_load_entity: VariableEntity):
    mocker.spy(variable_load_entity, 'mark_as_assignment_target')

    assert len(assignment_entity.targets) == 0
    assert assignment_entity.number_of_targets == 0

    assignment_entity.add_target(variable_load_entity)

    assert assignment_entity.uses_unpacking is False
    assert len(assignment_entity.targets) == 1 and assignment_entity.targets[0] == variable_load_entity
    assert assignment_entity.number_of_targets == 1
    assert variable_load_entity.mark_as_assignment_target.call_count == 1


def test_assignment_add_tuple_target(mocker, assignment_entity: AssignmentEntity, tuple_entity, variable_load_entity: VariableEntity):
    tuple_entity.add_element(variable_load_entity)
    tuple_entity.add_element(variable_load_entity)

    mocker.spy(tuple_entity, 'mark_as_assignment_target')
    mocker.spy(tuple_entity, 'used_for_unpacking')

    assert len(assignment_entity.targets) == 0
    assert assignment_entity.number_of_targets == 0

    assignment_entity.add_target(tuple_entity)

    assert assignment_entity.uses_unpacking is True
    assert len(assignment_entity.targets) == 1 and assignment_entity.targets[0] == tuple_entity
    assert assignment_entity.number_of_targets == 2
    assert tuple_entity.mark_as_assignment_target.call_count == 1
    assert tuple_entity.used_for_unpacking.call_count == 1


def test_assignment_add_list_target(mocker, assignment_entity: AssignmentEntity, list_entity, variable_load_entity: VariableEntity):
    list_entity.add_element(variable_load_entity)
    list_entity.add_element(variable_load_entity)

    mocker.spy(list_entity, 'mark_as_assignment_target')
    mocker.spy(list_entity, 'used_for_unpacking')

    assert len(assignment_entity.targets) == 0
    assert assignment_entity.number_of_targets == 0

    assignment_entity.add_target(list_entity)

    assert assignment_entity.uses_unpacking is True
    assert len(assignment_entity.targets) == 1 and assignment_entity.targets[0] == list_entity
    assert assignment_entity.number_of_targets == 2
    assert list_entity.mark_as_assignment_target.call_count == 1
    assert list_entity.used_for_unpacking.call_count == 1

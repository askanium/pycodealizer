import ast
from typing import Any

from pycodealizer.constants import VARIABLE, ASSIGNMENT
from pycodealizer.entities.literals import NumberEntity, TupleEntity, ListEntity
from pycodealizer.entities.variables import VariableEntity


class AssignmentEntity(object):
    """Represents an assignment in Abstract Syntax Tree."""

    entity_type = ASSIGNMENT

    def __init__(self, node: ast.Assign):
        self.line_nr = node.lineno
        self.value = None
        self.value_type = None
        self.value_initialized = False  # needed to know when value is explicitly defined as `None`
        self.targets = []
        self.number_of_targets = 0
        self.uses_unpacking = False
        self.uses_list_for_unpacking = False
        self.uses_tuple_for_unpacking = False

    def add_value(self, entity: Any):
        """Add an entity that corresponds to the value of the assignment."""

        self.value = entity
        self.value_type = entity.entity_type

        entity.mark_as_assignment_value(self)

        self.value_initialized = True

    def add_target(self, entity: Any):
        """Add an entity instance as the target of the assignment.

        Multiple targets mean that this is a multiple assignment (e.g. ``a = b = 1``).

        A tuple or list target means that this is an unpacking assignment (e.g. ``a, b = (1, 2)``).
        """
        self.targets.append(entity)
        self.number_of_targets += 1

        if isinstance(entity, TupleEntity):
            self.uses_tuple_for_unpacking = True
        elif isinstance(entity, ListEntity):
            self.uses_list_for_unpacking = True

        if any([self.uses_tuple_for_unpacking, self.uses_list_for_unpacking]):
            entity.used_for_unpacking()
            self.uses_unpacking = True
            self.number_of_targets = self.number_of_targets - 1 + entity.nr_of_elements

        entity.mark_as_assignment_target(self)

    def __repr__(self):
        return f'Assignment: \n' \
               f'   on line: {self.line_nr}\n' \
               f'   with value: {self.value} (type {self.value_type})\n' \
               f'   and {self.number_of_targets} targets\n' \
               f'   uses unpacking: {self.uses_unpacking}'

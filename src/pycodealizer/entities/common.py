from collections.__init__ import defaultdict
from typing import Any, List

from pycodealizer.entities.expressions import CallEntity, IfExpressionEntity
from pycodealizer.entities.literals import NumberEntity, TupleEntity, ListEntity, SetEntity, StringEntity
from pycodealizer.entities.statements import AssignmentEntity
from pycodealizer.entities.variables import VariableEntity, StarredEntity


class Context(object):
    """Represents the context various entities are encountered in.

    There are two types of an instance of this class holds:

    1. **AST Context** The hierarchical structure of nodes in the
    abstract syntax tree.
    2. **Execution Context** The execution context of the python flow.

    Both contexts types are stored as stacks.
    """
    def __init__(self, module):
        self.execution_context = [module]
        self.ast_context = [module]

    def stack_execution_context(self, entity: Any):
        """Add an entity instance to the execution context."""
        self.execution_context.append(entity)

    def unstack_execution_context(self):
        """Remove the topmost entity from the execution context."""
        return self.execution_context.pop()

    def stack_ast_node(self, node: Any):
        """Add a node to the ast_context stack."""
        self.ast_context.append(node)

    def unstack_ast_node(self):
        """Remove last node from the ast context."""
        return self.ast_context.pop()

    @property
    def current_execution_context(self):
        return self.execution_context[-1]

    @property
    def current_ast_node(self):
        return self.ast_context[-1]


class Module(object):
    """Represents a file in which various occurrences happen."""

    def __init__(self, path: str):
        self.path = path

        self.variables: List = list()
        self.starred_variables: List = list()
        self.numbers: List = list()
        self.strings: List = list()
        self.tuples: List = list()
        self.lists: List = list()
        self.sets: List = list()
        self.calls: List = list()
        self.if_expressions: List = list()
        self.assignments: List = list()

        self.line_numbers = defaultdict(list)
        self.type_line_numbers = defaultdict(list)

    def add_variable(self, variable: VariableEntity):
        """Add the variable entity to the module.

        There are three actions that are happening:
            1. Add the variable to the list of variables encountered in the module.
            2. Add the variable to the list that corresponds to entities
            encountered on the line number the variable entity occurs in.
            3. Add the entity type of the variable to the list that corresponds
            to entity types per line numbers.

        :param VariableEntity variable: The variable entity to add to the module.
        """
        self.variables.append(variable)
        self.line_numbers[variable.line_nr].append(variable)
        self.type_line_numbers[variable.line_nr].append(variable.entity_type)

    def add_starred_variable(self, starred: StarredEntity):
        """Add the starred variable entity to the module.

        There are three actions that are happening:
            1. Add the starred variable to the list of variables encountered in the module.
            2. Add the starred variable to the list that corresponds to entities
            encountered on the line number the variable entity occurs in.
            3. Add the entity type of the starred variable to the list that corresponds
            to entity types per line numbers.

        :param StarredEntity starred: The starred variable entity to add to the module.
        """
        self.starred_variables.append(starred)
        self.line_numbers[starred.line_nr].append(starred)
        self.type_line_numbers[starred.line_nr].append(starred.entity_type)

    def add_number(self, number: NumberEntity):
        """Add the number and its type (integer, float or complex) to the module.

        There are three actions that are happening:
            1. Add the number to the list of numbers encountered in the module.
            2. Add the number to the list that corresponds to entities
            encountered on the line number the number entity occurs in.
            3. Add the type of the number to the list that corresponds
            to entity types per line numbers.

        :param NumberEntity number: The number entity to add to the module.
        """
        self.numbers.append(number)
        self.line_numbers[number.line_nr].append(number)
        self.type_line_numbers[number.line_nr].append(number.value_type)

    def add_string(self, string: StringEntity):
        """Add the string to the module.

        There are three actions that are happening:
            1. Add the string to the list of strings encountered in the module.
            2. Add the string to the list that corresponds to entities
            encountered on the line number the string entity occurs in.
            3. Add the entity type of the string to the list that corresponds
            to entity types per line numbers.

        :param StringEntity string: The string entity to add to the module.
        """
        self.strings.append(string)
        self.line_numbers[string.line_nr].append(string)
        self.type_line_numbers[string.line_nr].append(string.entity_type)

    def add_tuple(self, tuple_: TupleEntity):
        """Add the tuple to the module.

        There are three actions that are happening:
            1. Add the tuple to the list of tuples encountered in the module.
            2. Add the tuple to the list that corresponds to entities
            encountered on the line number the tuple entity occurs in.
            3. Add the entity type of the tuple to the list that corresponds
            to entity types per line numbers.

        :param TupleEntity tuple_: The tuple entity to add to the module.
        """
        self.tuples.append(tuple_)
        self.line_numbers[tuple_.line_nr].append(tuple_)
        self.type_line_numbers[tuple_.line_nr].append(tuple_.entity_type)

    def add_list(self, list_: ListEntity):
        """Add the list to the module.

        There are three actions that are happening:
            1. Add the list to the list of lists encountered in the module.
            2. Add the list to the list that corresponds to entities
            encountered on the line number the list entity occurs in.
            3. Add the entity type of the list to the list that corresponds
            to entity types per line numbers.

        :param ListEntity list_: The list entity to add to the module.
        """
        self.lists.append(list_)
        self.line_numbers[list_.line_nr].append(list_)
        self.type_line_numbers[list_.line_nr].append(list_.entity_type)

    def add_set(self, set_: SetEntity):
        """Add the set to the module.

        There are three actions that are happening:
            1. Add the set to the list of sets encountered in the module.
            2. Add the set to the list that corresponds to entities
            encountered on the line number the set entity occurs in.
            3. Add the entity type of the set to the list that corresponds
            to entity types per line numbers.

        :param SetEntity set_: The set entity to add to the module.
        """
        self.sets.append(set_)
        self.line_numbers[set_.line_nr].append(set_)
        self.type_line_numbers[set_.line_nr].append(set_.entity_type)

    def add_assignment(self, assignment: AssignmentEntity):
        """Add the assignment to the module.

        There are three actions that are happening:
            1. Add the assignment to the list of assignments encountered in the module.
            2. Add the assignment to the list that corresponds to entities
            encountered on the line number the assignment entity occurs in.
            3. Add the entity type of the assignment to the list that corresponds
            to entity types per line numbers.

        :param AssignmentEntity assignment: The assignment entity to add to the module.
        """
        self.assignments.append(assignment)
        self.line_numbers[assignment.line_nr].append(assignment)
        self.type_line_numbers[assignment.line_nr].append(assignment.entity_type)

    def add_call(self, call: CallEntity):
        """Add the call to the module.

        There are three actions that are happening:
            1. Add the call to the list of calls encountered in the module.
            2. Add the call to the list that corresponds to entities
            encountered on the line number the call entity occurs in.
            3. Add the entity type of the call to the list that corresponds
            to entity types per line numbers.

        :param CallEntity call: The call entity to add to the module.
        """
        self.calls.append(call)
        self.line_numbers[call.line_nr].append(call)
        self.type_line_numbers[call.line_nr].append(call.entity_type)

    def add_if_expression(self, if_expression: IfExpressionEntity):
        """Add the if expression to the module.

        There are three actions that are happening:
            1. Add the if_expression to the list of if_expressions encountered in the module.
            2. Add the if_expression to the list that corresponds to entities
            encountered on the line number the if_expression entity occurs in.
            3. Add the entity type of the if_expression to the list that corresponds
            to entity types per line numbers.

        :param IfExpressionEntity if_expression: The if_expression entity to add to the module.
        """
        self.if_expressions.append(if_expression)
        self.line_numbers[if_expression.line_nr].append(if_expression)
        self.type_line_numbers[if_expression.line_nr].append(if_expression.entity_type)

    def __str__(self):
        result = f'Module: {self.path}\n' \
                 f'    Variables: {self.variables}\n' \
                 f'    Numbers: {self.numbers}\n' \
                 f'    Strings: {self.strings}\n' \
                 f'    Tuples: {self.tuples}\n' \
                 f'    Lists: {self.lists}\n' \
                 f'    Assignments: {self.assignments}\n' \
                 f'\n' \
                 f'    Line Numbers: {self.line_numbers}'
        return result

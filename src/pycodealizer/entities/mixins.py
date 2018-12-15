class LiteralsMixin(object):
    """Define common attributes and methods for literal entities.

    It contains flags related to usage in different expressions and/or contexts
    as well as methods to set those attributes.
    """

    def __init__(self):
        self.used_in_list = False
        self.used_in_tuple = False
        self.used_in_set = False
        self.used_in_if_statement = False
        self.used_in_for_statement = False
        self.used_in_while_statement = False
        self.used_in_function_call = False
        self.used_in_function_definition = False

        super().__init__()

    def mark_as_used_in_list(self):
        self.used_in_list = True

    def mark_as_used_in_tuple(self):
        self.used_in_tuple = True

    def mark_as_used_in_set(self):
        self.used_in_set = True

    def mark_as_used_in_if_statement(self):
        self.used_in_if_statement = True

    def mark_as_used_in_for_statement(self):
        self.used_in_for_statement = True

    def mark_as_used_in_while_statement(self):
        self.used_in_while_statement = True

    def mark_as_used_in_function_call(self):
        self.used_in_function_call = True

    def mark_as_used_in_function_definition(self):
        self.used_in_function_definition = True

    def mark_as_participating_as_keyword_arg(self, in_function_call=False, in_function_def=False):
        self.used_in_function_call = in_function_call
        self.used_in_function_definition = in_function_def


class StarredMixin(object):
    """Define functionality for entities that can be starred in python.

    Most common case is a [double] starred variable, like ``*[*]var``, but it can
    also be a [double] starred function call ``*[*]fn()`` or starred list ``*[1, 2, 3]``
    or double starred dict ``**{"a": 1}`` or something else.
    """

    def __init__(self):
        self.is_starred = False
        self.is_double_starred = False

    def mark_as_starred(self):
        """Mark the instance as being a starred entity."""
        self.is_starred = True

    def mark_as_double_starred(self):
        """Mark the instance as being a double starred entity."""
        self.is_double_starred = True


class AssignmentMixin(object):
    """Define common attributes and methods for assignments."""

    def __init__(self):
        self.is_assignment_target = False
        self.is_assignment_value = False
        self.assignment = None

    def mark_as_assignment_target(self, assignment):
        """Mark the instance as being the target of an assignment statement.

        :param assignment: The AssignmentEntity the target is part of.
        """
        self.is_assignment_target = True
        self.assignment = assignment

    def mark_as_assignment_value(self, assignment):
        """Mark the instance as being the value of an assignment statement.

        :param assignment: The AssignmentEntity the value is part of.
        """
        self.is_assignment_value = True
        self.assignment = assignment


class IfMixin(object):
    """Define common attributes and methods related to being
    part of an "if/elif/else" statement.
    """

    def __init__(self):
        self.is_part_of_if_test_condition = False
        self.is_part_of_if_body = False
        self.is_part_of_if_orelse = False

        # if expression is an expression of form "a if b else c"
        # if this is false, then the entity is part of a block level if expression
        self.is_part_of_an_if_expression = False

    def mark_as_part_of_if_test_condition(self, inside_if_expression=False):
        self.is_part_of_if_test_condition = True
        self.is_part_of_an_if_expression = inside_if_expression

    def mark_as_part_of_if_body(self, inside_if_expression=False):
        self.is_part_of_if_body = True
        self.is_part_of_an_if_expression = inside_if_expression

    def mark_as_part_of_if_orelse(self, inside_if_expression=False):
        self.is_part_of_if_orelse = True
        self.is_part_of_an_if_expression = inside_if_expression


class CommonMixin(LiteralsMixin, StarredMixin, AssignmentMixin, IfMixin):
    pass

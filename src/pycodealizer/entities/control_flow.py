from pycodealizer.constants import IF


class If(object):
    """Represents an if/elif/else conditional statement."""

    entity_type = IF

    def __init__(self, lineno: int):
        self.line_nr = lineno
        self.number_of_lines_in_body = 0

        self.comparison_to_numbers = 0
        self.comparison_to_strings = 0
        self.comparison_to_booleans = 0
        self.comparison_to_variables = 0
        self.comparison_to_none = 0

        self.function_calls = 0
        self.method_calls = 0

        self.equality_comparison = 0
        self.inequality_comparison = 0
        self.greater_comparison = 0
        self.greater_or_equal_comparison = 0
        self.smaller_comparison = 0
        self.smaller_or_equal_comparison = 0

        self.number_of_elifs = 0
        self.number_of_ands = 0
        self.number_of_ors = 0
        self.number_of_nots = 0

        self.ifs_in_body = []

        self.has_else_block = False
        self.is_inside_loop = False

    @property
    def single_condition(self):
        pass

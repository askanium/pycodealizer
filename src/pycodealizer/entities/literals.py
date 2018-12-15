import ast
from typing import Any

from pycodealizer.constants import NUMBER, TUPLE, LIST, STRING, SET
from pycodealizer.entities.mixins import CommonMixin


class NumberEntity(CommonMixin):

    entity_type = NUMBER

    def __init__(self, node: ast.Num):
        self.line_nr = node.lineno
        self.value = node.n
        self.value_type = node.n.__class__.__name__

        super().__init__()

    def __repr__(self):
        return f'{self.value_type}: {self.value}'


class StringEntity(CommonMixin):

    entity_type = STRING

    def __init__(self, node: ast.Str):
        self.line_nr = node.lineno
        self.value = node.s
        self.value_length = len(node.s)

        super().__init__()

    def __repr__(self):
        return f'{self.value} ({self.value_length} chars)'


class TupleEntity(CommonMixin):

    entity_type = TUPLE

    def __init__(self, node: ast.Tuple):
        self.line_nr = node.lineno
        self.context = node.ctx.__class__.__name__

        self.elements = list()

        super().__init__()

    def add_element(self, element: Any):
        self.elements.append(element)
        element.mark_as_used_in_tuple()

    def used_for_unpacking(self):
        for element in self.elements:
            try:
                element.mark_as_participating_in_unpacking(in_tuple=True)
            except AttributeError:
                print(f'{element} cannot be marked as participating in unpacking')

    @property
    def nr_of_elements(self):
        return len(self.elements)


class ListEntity(CommonMixin):

    entity_type = LIST

    def __init__(self, node: ast.List):
        self.line_nr = node.lineno
        self.context = node.ctx.__class__.__name__

        self.elements = list()

        super().__init__()

    def add_element(self, element: Any):
        self.elements.append(element)
        element.mark_as_used_in_list()

    def used_for_unpacking(self):
        for element in self.elements:
            try:
                element.mark_as_participating_in_unpacking(in_list=True)
            except AttributeError:
                print(f'{element} cannot be marked as participating in unpacking')

    @property
    def nr_of_elements(self):
        return len(self.elements)


class SetEntity(CommonMixin):

    entity_type = SET

    def __init__(self, node: ast.Set):
        self.line_nr = node.lineno

        self.elements = list()

        super().__init__()

    def add_element(self, element: Any):
        self.elements.append(element)
        element.mark_as_used_in_set()

    @property
    def nr_of_elements(self):
        return len(self.elements)

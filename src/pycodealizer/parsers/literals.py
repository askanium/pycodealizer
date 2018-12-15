import ast
from typing import Any, Dict

from pycodealizer.constants import IS_PART_OF_TUPLE, IS_PART_OF_LIST
from pycodealizer.entities.common import Module, Context
from pycodealizer.entities.literals import TupleEntity, ListEntity, NumberEntity, SetEntity, StringEntity
from pycodealizer.parsers.base import EntityParser


class BaseSequenceParser(EntityParser):
    """Parses nodes that represent either a List or a Tuple."""

    def parse(self, node: Any, module: Module, context: Context):
        """Process one of `[ast.List, ast.Tuple]` nodes and extract relevant stats.

        Tuple and List nodes have two fields:
            - `elts` that represents the elements of the array
            - `ctx` that represents the context under which the array is used (Store or Load)
        """
        entity = self.create_new_entity(node)
        context.stack_ast_node(entity)

        # if isinstance(node.ctx, ast.Store):
        #     context[UNPACKING_VALUES] = True


        # existing_context = set()
        # for key in context:
        #     if key in IS_PART_OF_MAPPER:
        #         existing_context.add(IS_PART_OF_MAPPER[key])
        #
        # # create a hierarchy of which
        # if self.node_type not in context:
        #     context[self.node_type] = ''
        #     delimiter = ''
        #     last_node_type_appearance = 0
        # else:
        #     delimiter = '_'
        #     last_node_type_appearance = len(context[self.node_type].split('_')) - 1  # remove 1 that is going to be accounted for in the intersection statement
        #
        # context[self.node_type] = f'{context[self.node_type]}' \
        #                           f'{delimiter}' \
        #                           f'{len(existing_context.intersection(COMPLEX_DATA_TYPES)) + 1 + last_node_type_appearance}'

        for element in node.elts:
            parser = self.get_parser(element)
            element_entity = parser.parse(element, module, context)
            entity.add_element(element_entity)

        context.unstack_ast_node()

        self.add_entity_to_module(entity, module, context)

        return entity

    def create_new_entity(self, node: Any):
        raise NotImplementedError('The create_new_entity method should be implemented in the inheriting class.')

    def add_entity_to_module(self, entity: Any, module: Module):
        """Adds the node as either a List or a Tuple to the current module.

        :param entity: The entity instance.
        :param module: The python module where this variable is encountered.
        """
        raise NotImplemented('The add_entity_to_module method should be implemented in inheriting class.')


class TupleParser(BaseSequenceParser):
    """Parses tuple nodes."""

    def __init__(self):
        self.node_type = IS_PART_OF_TUPLE

    def create_new_entity(self, node: ast.Tuple):
        return TupleEntity(node)

    def add_entity_to_module(self, entity: TupleEntity, module: Module):
        module.add_tuple(entity)


class ListParser(BaseSequenceParser):
    """Parses list nodes."""

    def __init__(self):
        self.node_type = IS_PART_OF_LIST

    def create_new_entity(self, node: ast.List):
        return ListEntity(node)

    def add_entity_to_module(self, entity: ListEntity, module: Module):
        module.add_list(entity)


class SetParser(BaseSequenceParser):
    """Parses set nodes."""

    def create_new_entity(self, node: ast.Set):
        return SetEntity(node)

    def add_entity_to_module(self, entity: SetEntity, module: Module):
        module.add_set(entity)


class NumberParser(EntityParser):
    """Parses ``ast.Num`` nodes that represent all types of numbers."""

    def parse(self, node: ast.Num, module: Module, context: Context):
        """Process an ``ast.Num`` code and identify which type of number does it hold.
        """
        number_entity = NumberEntity(node)
        module.add_number(number_entity)

        return number_entity


class StringParser(EntityParser):
    """Parses ``ast.Str`` nodes that represent strings."""

    def parse(self, node: ast.Str, module: Module, context: Context):
        """Process an ``ast.Str`` code and identify which type of number does it hold.
        """
        string_entity = StringEntity(node)
        module.add_string(string_entity)

        return string_entity


number_parser = NumberParser()
string_parser = StringParser()
tuple_parser = TupleParser()
list_parser = ListParser()
set_parser = SetParser()

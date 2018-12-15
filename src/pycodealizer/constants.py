from enum import Enum

from pycodealizer.datatypes import DataTypes

LOAD_CONTEXT = 'load_context'
STORE_CONTEXT = 'store_context'
DEL_CONTEXT = 'del_context'

# Contexts related to statistics per module.
UNPACKING_VALUES = 'unpacking_values'
MULTIPLE_ASSIGNMENT = 'multiple_assignment'

IS_PART_OF_TUPLE = 'is_part_of_tuple'
IS_PART_OF_LIST = 'is_part_of_list'
IS_PART_OF_SET = 'is_part_of_set'
IS_PART_OF_DICT = 'is_part_of_dict'

IS_PART_OF_MAPPER = {
    IS_PART_OF_TUPLE: DataTypes.TUPLE,
    IS_PART_OF_LIST: DataTypes.LIST,
    IS_PART_OF_SET: DataTypes.SET,
    IS_PART_OF_DICT: DataTypes.DICT
}

VARIABLE = 'variable'
STARRED_VAR = 'starred_variable'
NUMBER = 'number'
STRING = 'string'
TUPLE = 'tuple'
LIST = 'list'
SET = 'set'
DICT = 'dict'
FUNCTION = 'function'
ATTRIBUTE = 'attribute'

ASSIGNMENT = 'assignment'
CALL = 'call'
IF = 'if'
IF_EXPRESSION = 'if_expression'
KEYWORD_ARGUMENT = 'kwarg'


class UsageContexts(Enum):
    LOAD = 'Load'
    STORE = 'Store'
    DELETE = 'Del'

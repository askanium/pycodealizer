from enum import Enum


class DataTypes(Enum):
    STRING = 'Str'
    NUMBER = 'Num'  # integer, float or complex, all fall under this `ast.Num` node type.
    BYTES = 'Bytes'
    LIST = 'List'
    TUPLE = 'Tuple'
    DICT = 'Dict'
    SET = 'Set'
    ELLIPSIS = 'Ellipsis'
    NAME_CONSTANT = 'NameConstant'  # True, False and None, all fall under this ast node.
    FORMATTED_VALUE = 'FormattedValue'
    JOINED_STRING = 'JoinedStr'


COMPLEX_DATA_TYPES = {DataTypes.LIST, DataTypes.TUPLE, DataTypes.DICT, DataTypes.SET}

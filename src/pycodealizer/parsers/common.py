from collections import namedtuple

from pycodealizer.parsers.base import not_implemented_parser
from pycodealizer.parsers.expressions import call_parser, if_expression_parser
from pycodealizer.parsers.literals import number_parser, string_parser, tuple_parser, list_parser, set_parser
from pycodealizer.parsers.statements import assignment_parser
from pycodealizer.parsers.variables import variable_parser, starred_parser

ParsersNT = namedtuple('Parsers', [
    'Name_parser',
    'Assign_parser',
    'Num_parser',
    'Str_parser',
    'Tuple_parser',
    'List_parser',
    'Set_parser',
    'Starred_parser',
    'Call_parser',
    'IfExp_parser',
    'not_implemented_parser'
])

Parsers = ParsersNT(
    variable_parser,
    assignment_parser,
    number_parser,
    string_parser,
    tuple_parser,
    list_parser,
    set_parser,
    starred_parser,
    call_parser,
    if_expression_parser,
    not_implemented_parser
)

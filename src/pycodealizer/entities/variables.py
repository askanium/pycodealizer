import ast

from pycodealizer.constants import VARIABLE, STARRED_VAR
from pycodealizer.entities.mixins import CommonMixin


class VariableEntity(CommonMixin):
    """Represent a variable in Python code.

    Variable nodes have two relevant field:
        - ``id`` that represents the name of the variable
        - ``ctx`` that represents the context the variable is used in, which can be of three types:
            - ``ast.Load`` means the variable is used to load its value
            - ``ast.Store`` means the variable is used to store some value
            - ``ast.Del`` means the variable is going to be deleted
    """

    entity_type = VARIABLE

    def __init__(self, node: ast.Name):
        self.line_nr = node.lineno
        self.name = node.id
        self.context = node.ctx.__class__.__name__

        self.used_in_unpacking_assignment = False

        super().__init__()

    def __repr__(self):
        return f'Variable: {self.name}'

    def mark_as_participating_in_unpacking(self, in_tuple=False, in_list=False):
        self.used_in_unpacking_assignment = True

        if in_tuple:
            self.used_in_tuple = True

        if in_list:
            self.used_in_list = True

    def mark_as_participating_as_keyword_arg(self, in_function_call=False, in_function_def=False, is_double_starred=False):
        if is_double_starred:
            self.mark_as_double_starred()
        super().mark_as_participating_as_keyword_arg(in_function_call=in_function_call, in_function_def=in_function_def)


class StarredEntity(object):
    """Represent a starred variable reference (e.g. ``*var``).

    Has the following fields:
        - ``value`` that holds the variable (typically a `ast.Name` node)
        - ``ctx`` the context under which the starred variable is used

    Note that this entity type is used only in ``ast.Call`` nodes in Python 3.5 and above.
    For ``ast.FunctionDef`` there is another definition for ``*var`` declaration.
    """

    entity_type = STARRED_VAR

    def __init__(self, node: ast.Starred):
        self.line_nr = node.lineno
        self.value = None
        self.context = node.ctx.__class__.__name__

    def set_value_entity(self, entity):
        """Add value entity.

        As entity classes do not directly handle AST node instances and as the class entity
        type is created before any children entities are instantiated, there is no way to
        know which class does the ``node.value`` is going to be. Therefore, it is being added
        later with this method.
        """
        self.value = entity

        try:
            self.value.mark_as_starred()
        except AttributeError:
            print(f'*************** {self.value.entity_type} has no "mark_as_starred()" method.')

    @property
    def name(self):
        """Proxies the name of the value that it holds."""
        return self.value.name

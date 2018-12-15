from collections import defaultdict

from pycodealizer.constants import LOAD_CONTEXT, STORE_CONTEXT, DEL_CONTEXT, MULTIPLE_ASSIGNMENT, UNPACKING_VALUES, \
    IS_PART_OF_TUPLE, IS_PART_OF_LIST, IS_PART_OF_DICT, IS_PART_OF_SET


class classdefaultdict(defaultdict):
    """Allows setting a class instance that is passed the `key` argument
    upon instance initialization.
    """
    def __missing__(self, key):
        """Initialize the `defaultdict.default_factory` class with the key.

        Create an instance of the `defaultdict.default_factory` class with
        the `key` that is used to store the class instance in the dict.

        :param key: The key under which to store the value in the defaultdict object.
        :return: The initialized instance of the `defaultdict.default_factory` class.
        """
        self[key] = self.default_factory(key)
        return self[key]


class variablebinaryrepresentationdict(defaultdict):
    """

    """
    variable_fields = [
        LOAD_CONTEXT,
        STORE_CONTEXT,
        DEL_CONTEXT,
        MULTIPLE_ASSIGNMENT,
        UNPACKING_VALUES,
        IS_PART_OF_TUPLE,
        IS_PART_OF_LIST,
        IS_PART_OF_DICT,
        IS_PART_OF_SET
    ]

    def binary_repr(self):
        representation = 0b0
        for i, field in enumerate(self.variable_fields):
            representation += (field in self) << len(self.variable_fields) - i - 1

        return '{0:b}'.format(representation)

    def __repr__(self):
        result = super().__repr__()
        result += ' {0:{fill}{align}{len}}'.format(self.binary_repr(), fill='0', align='>', len=len(self.variable_fields))
        return result

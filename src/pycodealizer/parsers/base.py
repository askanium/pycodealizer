import abc
from typing import Any, Dict

from pycodealizer.entities.common import Module, Context


class AbstractEntityParser(abc.ABC):

    @abc.abstractmethod
    def parse(self, node: Any, module: Module, context: Context):
        for field in node._fields:
            method = getattr(self, f'parse_{field}')
            method(getattr(node, field), module, context)


class BaseEntityParser(object):

    _parsers = None

    def get_parser(self, node: Any):
        return getattr(self.parsers, f'{node.__class__.__name__}_parser', self.parsers.not_implemented_parser)

    def __getattribute__(self, item):
        if item == 'parsers':
            # Lazy Parsers initialization to overcome circular dependencies.
            if not self._parsers:
                import importlib
                mod = importlib.import_module('.common', package='pycodealizer.parsers')
                self._parsers = mod.Parsers
            return self._parsers
        return super().__getattribute__(item)


class EntityParser(AbstractEntityParser, BaseEntityParser, abc.ABC):
    pass


class NotImplementedParser(EntityParser):
    def parse(self, node: Any, module: Module, context: Dict[str, Any]):
        print(f"*********** Don't know how to process {node.__class__.__name__} nodes. ***********")


not_implemented_parser = NotImplementedParser()


class Parser(BaseEntityParser):

    def __init__(self):
        self.modules = list()

    def parse(self, node: Any):
        """Process the given node and extract relevant info from it."""
        parser = self.get_parser(node)
        parser.parse(node, self.modules[-1], Context(self.modules[-1]))

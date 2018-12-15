import abc
from typing import Any

# from pycodealizer.parsers import Aggregators


class CodeStatisticsAggregator(object):
    """Aggregates various types of info about code."""

    def __init__(self):
        self.aggregators = Aggregators()
        self.modules = list()

    def process_node(self, node: Any, **kwargs):
        """Process the given node and extract relevant info from it."""
        for aggregator_name in self.get_processing_methods(node):
            aggregator = getattr(self.aggregators, aggregator_name)
            aggregator.process(node, self.modules[-1], **kwargs)

    @staticmethod
    def get_processing_methods(node: Any):
        """Get the relevant methods to process the given node.

        :param node: The Abstract Syntax Tree node for which to get processing methods.
        :return: The aggregators to which to pass the node.
        """
        node_type_to_aggregator_type_mapper = {
            'Name': ['variables'],
            'Assign': ['assignments']
        }

        return node_type_to_aggregator_type_mapper.get(node.__class__.__name__, [])

import ast

import sys

from pycodealizer.node_handlers import ASTNodeHandler
from pycodealizer.walkers import DirWalker, ModuleWalker

if __name__ == '__main__':
    path = sys.argv[1]
    walker = DirWalker(root_dir=path)
    nh = ASTNodeHandler()
    stw = ModuleWalker()
    for python_file in walker.walk():
        with open(python_file, 'r') as f:
            tree = ast.parse(f.read())
            nh.update_file_occurrence(python_file)
            for node in stw.walk(tree):
                nh.handle_node(node)
    for module in nh.parser.modules:
        print(module)

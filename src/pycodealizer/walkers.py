import ast
import os


class DirWalker(object):

    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def walk(self):
        """Walks the subdirectories and files in the root directory."""
        return self.scan_directory(self.root_dir)

    def scan_directory(self, dir_name: str):
        """Scan a specific directory.

        :param dir_name The directory name to scan for python files.
        """
        for dirpath, dirnames, filenames in os.walk(dir_name):
            # print(dirpath, dirnames, filenames)

            for filename in filenames:
                if filename.endswith(('.py', '.pyw')):
                    filepath = os.path.join(dirpath, filename)
                    yield filepath

            for dirname in dirnames:
                self.scan_directory(os.path.join(dirpath, dirname))


class ModuleWalker(object):
    """Walks along the children of an `ast.Module` node."""

    @staticmethod
    def walk(tree_root: ast.Module):
        """Yield the immediate children of the `ast.Module` node.

        :param tree_root: The root of the abstract syntax tree to parse.
        """
        for child in ast.iter_child_nodes(tree_root):
            yield child

import os
from pathlib import Path

from PythonC.symbolTree.tree import SymbolTree


class Compiler:
    def __init__(self, target: str, root: str = None) -> None:
        if root is not None:
            self.root = Path(root)
            target = self.root / target
        self.target = Path(target).absolute()
        if root is None:
            self.root = self.target.parent
        self.symbolTree = SymbolTree()

    def compile(self):
        self.symbolTree.generateTree(self.root)
        self.symbolTree.inferTypes()

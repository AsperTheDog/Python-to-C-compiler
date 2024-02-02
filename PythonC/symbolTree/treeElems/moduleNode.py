from __future__ import annotations

from PythonC.elements.importElem import Import
from PythonC.symbolTree.treeElems.baseNode import BaseNode


class ModuleNode(BaseNode):
    class RelativeImport:
        def __init__(self, node: BaseNode, alias: str):
            self.node = node
            self.alias = alias

    importRegex = r"^(?:from ([\w\d.]+) )?import ((?:[\w\d.]|, )+|\*)(?: as ([\w\d]+))?"

    def __init__(self, name: str, uniqueID: int, parent: BaseNode):
        super().__init__(name, uniqueID, parent)
        self.mainFunc = None
        self.imports = []
        self.relativeExterns = []

    def resolveImports(self):
        tmpElems = set()
        for imp in self.imports:
            root = self.parent.route
            if imp.root is not None:
                routes = imp.root.split(".")
                dots = 0
                for route in routes:
                    if route != "":
                        break
                    dots += 1
                if dots == 1:
                    root = root + "." + imp.root.lstrip(".")
                elif dots > 1:
                    root = ".".join(root.split(".")[:-dots]) + imp.root.lstrip(".")
                else:
                    root = root + "." + imp.root
            elems = imp.getImportObjects(self.tree, root)
            for elem in elems:
                tmpElems.add(ModuleNode.RelativeImport(elem, imp.alias))
        self.imports = tmpElems

    def findImport(self, name: str) -> ModuleNode.RelativeImport:
        for imp in self.imports:
            if imp.alias is not None:
                if imp.alias == name:
                    return imp.node
            elif imp.node.name == name:
                return imp.node
        raise ValueError("Could not find import")
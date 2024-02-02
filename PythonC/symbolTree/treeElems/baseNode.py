from __future__ import annotations

from copy import copy


# Base class for the Symbol tree node. Provides some default behavior and variables for node traversal and search
class BaseNode:
    def __init__(self, name: str, uniqueID: int, parent: BaseNode = None):
        self.name = name
        self.children: dict[str: BaseNode] = {}
        self.parent = parent
        self.route = parent.route + "." + name if parent else name

        from PythonC.symbolTree.tree import SymbolTree
        self.tree: SymbolTree = None if self.parent is None or self.parent.tree is None else self.parent.tree
        self.uniqueName = "obj_" + str(uniqueID)
        print(self.route, "->", self.uniqueName)

    # Adds a child
    def add(self, elem: BaseNode) -> bool:
        if elem.name in self.children:
            return False
        self.children[elem.name] = elem

    # Finds a specific node given a route
    def find(self, elems: list[str], scopeRestriction=None) -> BaseNode | None:
        nextElem = elems.pop(0)
        if nextElem != self.name:
            return None
        if len(elems) == 0:
            return self
        for child in self.children.values():
            ret = child.find(copy(elems))
            if ret is not None:
                return ret
        raise ValueError("Could not find specified route")

    # Infer types of the variables. This will traverse the whole tree processing the variable types and 
    # infering them based on their value
    def inferTypes(self):
        for child in self.children.values():
            child.inferTypes()

    def resolveImports(self):
        for child in self.children.values():
            child.resolveImports()


    def findParentModule(self):
        node = self
        from PythonC.symbolTree.treeElems.moduleNode import ModuleNode
        while not isinstance(node, ModuleNode):
            node = node.parent
            if node is None:
                raise ValueError("Could not find parent module")
        return node

from PythonC.symbolTree.treeElems.baseNode import BaseNode


class Import:
    def __init__(self, root: str, imports: str, alias: str) -> None:
        self.root: str = root
        self.targets: str = imports
        self.alias: str = alias

    def getImportObjects(self, tree, root: str) -> list[BaseNode]:
        if self.targets == "*":
            return tree.findElement(root).children.values()
        else:
            return [tree.findElement(root + "." + target) for target in self.targets.split(", ")]

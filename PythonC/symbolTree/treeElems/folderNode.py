from PythonC.symbolTree.treeElems.baseNode import BaseNode


class FolderNode(BaseNode):
    def __init__(self, name: str, parent: BaseNode):
        super().__init__(name, parent)

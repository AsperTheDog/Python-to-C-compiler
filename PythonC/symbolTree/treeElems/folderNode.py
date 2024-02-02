from PythonC.symbolTree.treeElems.baseNode import BaseNode


class FolderNode(BaseNode):
    def __init__(self, name: str, uniqueID: int, parent: BaseNode):
        super().__init__(name, uniqueID, parent)

from PythonC.elements.functionElem import Function
from PythonC.symbolTree.treeElems.baseNode import BaseNode


class ModuleNode(BaseNode):
    def __init__(self, name: str, parent: BaseNode):
        super().__init__(name, parent)
        self.mainFunc = None

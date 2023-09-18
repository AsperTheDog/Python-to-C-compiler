from PythonC.elements.classElem import Class
from PythonC.symbolTree.treeElems.baseNode import BaseNode


class ClassNode(BaseNode):
    def __init__(self, cls: Class, parent: BaseNode):
        super().__init__(cls.name, parent)
        self.cls = cls

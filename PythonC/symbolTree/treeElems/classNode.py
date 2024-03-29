from PythonC.elements.classElem import Class
from PythonC.symbolTree.treeElems.baseNode import BaseNode


class ClassNode(BaseNode):
    evaluateRegex = r"class ([\w\d]+)(?:\(((?:[\w\d]+(, )?)*)\))?:"

    def __init__(self, cls: Class, uniqueID: int, parent: BaseNode):
        super().__init__(cls.name, uniqueID, parent)
        self.cls = cls

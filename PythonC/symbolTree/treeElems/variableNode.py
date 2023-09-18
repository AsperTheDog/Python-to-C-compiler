from PythonC.elements.variableElem import Variable
from PythonC.symbolTree.treeElems.baseNode import BaseNode


class VariableNode(BaseNode):
    def __init__(self, var: Variable, parent: BaseNode):
        super().__init__(var.name, parent)
        self.var = var

    def inferTypes(self):
        self.var.inferFromValue(self)

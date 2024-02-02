from PythonC.elements.variableElem import Variable
from PythonC.symbolTree.treeElems.baseNode import BaseNode


class VariableNode(BaseNode):
    evaluateRegex = r"^\s*(\w+)(?:: (\w+))? = (.+)$"
    objEvaluateRegex = r"^\s*self\.(\w+)(?:: (\w+))? = (.+)$"

    def __init__(self, var: Variable, uniqueID: int, parent: BaseNode):
        super().__init__(var.name, uniqueID, parent)
        self.var = var

    def inferTypes(self):
        self.var.inferFromValue(self)

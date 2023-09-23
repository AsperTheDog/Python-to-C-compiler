from PythonC.elements.functionElem import Function
from PythonC.symbolTree.treeElems.baseNode import BaseNode


class FunctionNode(BaseNode):
    evaluateRegex = r"def (\w+)\(((?:\w+: [[\]\w]+(?: = .+?)?(?:, )?)*)\)(?: -> (\w+))?:"
    objEvaluateRegex = r"def (\w+)\((self)?((?:(?:, )?\w+: [[\]\w]+(?: = .+?)?)*)\)(?: -> (\w+))?:"

    def __init__(self, func: Function, parent: BaseNode):
        super().__init__(func.name, parent)
        self.func = func

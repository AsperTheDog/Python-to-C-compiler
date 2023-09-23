import re
from enum import Enum

from PythonC.symbolTree.treeElems.baseNode import BaseNode


class VarScope(Enum):
    GLOBAL = 0
    MAIN = 1
    FUNCTION = 2
    CLASS = 3
    OBJECT = 4


class VarType(Enum):
    INT = (r"[0-9]+", "int")
    DOUBLE = (r"[0-9]+\.[0-9]+", "double")
    STRING = (r"([\"'])(?:(?=(\\?))\2.)*?\1", "std::string")
    BOOL = (r"(?:False)|(?:True)", "bool")
    # LIST = (r"\[(.*)]", "TODO")
    # TUPLE = (r"\((.*?,.*?)\)", "TODO")
    # DICT TODO
    OBJ = (r".+", "%meta%")

    @staticmethod
    def findFromStr(arg: str):
        if arg is None:
            return None
        typeDict = {
            "int": VarType.INT,
            "float": VarType.DOUBLE,
            "str": VarType.STRING,
            "bool": VarType.BOOL,
        }
        if arg in typeDict:
            return typeDict[arg]
        return VarType.OBJ


class Variable:
    def __init__(self, name: str, scope: VarScope, hintedType: VarType | None, value: str | None):
        self.name = name
        self.type = hintedType.value[1] if hintedType is not None else None
        self.value = value
        self.scope = scope
        if self.type is None and self.value is None:
            SyntaxError("Variables must have either type hint or default value")

    def inferTypeFromObj(self, node: BaseNode):
        try:
            varName = self.value
            match = re.fullmatch(r"([\w\d.]+)\(.*\)", varName)
            if match is not None:
                varName = match.group(1)
            valueNode = node.tree.findElement(node.parent.route + "." + varName)

            from PythonC.symbolTree.treeElems.variableNode import VariableNode
            from PythonC.symbolTree.treeElems.functionNode import FunctionNode
            from PythonC.symbolTree.treeElems.classNode import ClassNode
            if isinstance(valueNode, VariableNode):
                valueNode.var.inferFromValue(valueNode)
                self.type = valueNode.var.type
            elif isinstance(valueNode, FunctionNode):
                if valueNode.func.ret is None:
                    raise SyntaxError("Tried to assign return value of void function")
                self.type = valueNode.func.ret
            return
        except ValueError:
            pass

    def inferFromValue(self, node: BaseNode):
        if self.type is not None:
            return
        for varType in VarType:
            if re.fullmatch(varType.value[0], self.value):
                self.type = varType
                break
        if self.type != VarType.OBJ:
            return
        self.inferTypeFromObj(node)
        # raise SyntaxError("Invalid variable type, could not infer type")

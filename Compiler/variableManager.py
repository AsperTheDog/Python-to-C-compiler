import re
from dataclasses import dataclass
from enum import StrEnum

from Compiler.expressionParser import ExpressionParser


class VarTypes(StrEnum):
    INT = "int",
    STR = "str",
    CHAR = "chr",
    FLOAT = "float",
    BOOL = "bool",
    CUSTOM = "%meta%"

    @classmethod
    def contains(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


@dataclass
class VariableData:
    name: str
    type: VarTypes
    assignmentType: str
    value: str
    extraData: str

    def __init__(self, name: str, varType: str, assignment: str, value: str, extraData: str = None):
        self.name = name
        if varType is None:
            self.type = None
        elif not VarTypes.contains(varType):
            self.type = VarTypes.CUSTOM
        else:
            self.type = VarTypes(varType)
        self.assignmentType = assignment
        self.value = value
        self.extraData = extraData


class VariableManager:
    def __init__(self, parent):
        self.codeManager = parent
        self.variableTable = {}

    def addVariableElem(self, varElem: VariableData):
        self.addVariable(varElem.name, varElem.type, varElem.value, varElem.extraData)

    def addVariable(self, name: str, varType: str, value: str, metadata: str = None) -> None:
        if varType is None:
            varType = VariableManager.deduceType(value)
        self.variableTable[name] = ((varType, metadata), value)

    def exists(self, name: str) -> bool:
        return name in self.variableTable

    @staticmethod
    def parse(snippet: str) -> list[VariableData]:
        match = re.match(r"([\w.]+)(?:: (\w+|\w*(?:\[[\w, ]*])?))? (=|\+=|-=|\*=|/=|%=|//=) (.+)", snippet)
        if match is not None:
            return [VariableData(match.group(1), match.group(2), match.group(3), match.group(4))]
        match = re.match(r"((?:[\w.](?:, )?)+) = (.+)", snippet)
        if match is not None:
            variables = match.group(1).split(", ")
            expressions = ExpressionParser.divideExpressions(match.group(2), len(variables))
            varsElems = []
            for name, value in zip(variables, expressions):
                varsElems.append(VariableData(name, None, "=", value))
            return varsElems
        return []

    @staticmethod
    def deduceType(value: str) -> VarTypes | None:
        pass

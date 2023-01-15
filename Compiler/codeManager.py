import re
from enum import Enum

from Compiler.classManager import ClassManager
from Compiler.functionManager import FunctionManager
from Compiler.variableManager import VariableManager, VariableData


class ScopeTypes(Enum):
    FUNCTION = 0,
    CLASS = 1


class CodeManager:
    def __init__(self):
        self.code = ""
        self.mainVariables = VariableManager(self)
        self.classes = ClassManager()
        self.functions = FunctionManager()
        self.scoped: (ScopeTypes, str, str, list[str]) = None

    def addCodeFront(self, name: str, newSnippet: str):
        nameComment = "\n# Snippet added: " + name + "\n"
        self.code = nameComment + newSnippet + self.code

    def addCodeBack(self, name: str, newSnippet: str):
        nameComment = "\n# Snippet added: " + name + "\n"
        self.code += nameComment + newSnippet

    def gatherSymbols(self):
        for line in self.code.split("\n"):
            if self.scoped:
                tabs = CodeManager.getTabs(line)
                if tabs == 0:
                    if self.scoped[0] == ScopeTypes.FUNCTION:
                        self.functions.add(self.scoped[1], self.scoped[2], self.scoped[3])
                    else:
                        self.classes.add(self.scoped[1], self.scoped[2], self.scoped[3])
                    self.scoped = None
                else:
                    self.scoped[3].append(line)
                    continue
            match = ClassManager.parse(line)
            if match is not None:
                self.scoped = (ScopeTypes.CLASS, match.group(1), match.group(2), [])
                continue
            match = FunctionManager.parse(line)
            if match is not None:
                self.scoped = (ScopeTypes.FUNCTION, match.group(1), match.group(2), [])
                continue
            matchList: list[VariableData] = self.mainVariables.parse(line)
            for var in matchList:
                if var.assignmentType == "=" and not self.mainVariables.exists(var.name):
                    self.mainVariables.addVariableElem(var)


    @staticmethod
    def getTabs(line: str):
        count = 0
        for elem in line:
            if elem != ' ':
                return count
            count += 1

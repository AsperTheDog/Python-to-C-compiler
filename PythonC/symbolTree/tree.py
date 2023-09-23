from __future__ import annotations

from pathlib import Path
import re

from PythonC.elements.classElem import Class
from PythonC.elements.functionElem import Function, FuncType
from PythonC.elements.variableElem import Variable, VarType, VarScope

from PythonC.symbolTree.treeElems.baseNode import BaseNode
from PythonC.symbolTree.treeElems.classNode import ClassNode
from PythonC.symbolTree.treeElems.folderNode import FolderNode
from PythonC.symbolTree.treeElems.functionNode import FunctionNode
from PythonC.symbolTree.treeElems.moduleNode import ModuleNode
from PythonC.symbolTree.treeElems.variableNode import VariableNode

import autopep8


class ScopeHandler:
    class Scope:
        def __init__(self, element: Function | Class):
            self.element = element
            self.code = []

        def addLine(self, line: str):
            self.code.append(line)

        def retrieve(self):
            self.element.addCode(self.code)
            return self.element

    def __init__(self):
        self.scopes: list[ScopeHandler.Scope] = []
        self.push(Function("_main", FuncType.GLOBAL, [], None))

    def depth(self):
        return len(self.scopes) - 1

    def push(self, element: Function | Class):
        self.scopes.append(ScopeHandler.Scope(element))

    def addLine(self, line: str):
        tabs = (len(line) - len(line.lstrip())) / 4
        if tabs < self.depth():
            return False
        line = line[self.depth() * 4:]
        self.scopes[-1].addLine(line)
        return True

    def pop(self) -> Function | Class:
        scope = self.scopes.pop()
        return scope.retrieve()

    def isMain(self):
        return len(self.scopes) == 1


class SymbolTree:
    def __init__(self):
        self.root = FolderNode("root", None)

    def findElement(self, path: str) -> BaseNode:
        if path[-1] == '.':
            path = path[:-1]
        elems = path.split(".")
        return self.root.find(elems)

    def addElement(self, parentPath: str | BaseNode, node: BaseNode) -> None:
        parent = parentPath if isinstance(parentPath, BaseNode) else self.findElement(parentPath)
        node.tree = self
        parent.add(node)

    def inferTypes(self):
        self.root.inferTypes()

    def generateTree(self, path: Path):
        node = self.crawlFolder(path, self.root)
        self.root.add(node)

    def crawlFolder(self, path: Path, parent: BaseNode):
        rootNode = FolderNode(path.name, parent)
        dirs = [x for x in path.iterdir() if x.is_dir()]
        for path in dirs:
            node = self.crawlFolder(path, rootNode)
            rootNode.add(node)
        files = [x for x in path.iterdir() if x.is_file() and x.match("*.py")]
        for file in files:
            node = self.crawlFile(file, rootNode)
            rootNode.add(node)
        return rootNode

    def crawlFile(self, root: Path, parent: BaseNode):
        def popScope(scope: ScopeHandler, rootNode):
            elem = scope.pop()
            if isinstance(elem, Function):
                elem = self.crawlFunction(elem, rootNode)
            else:
                elem = self.crawlClass(elem, rootNode)
            self.addElement(rootNode, elem)

        with open(root, "r") as file:
            code = file.read()
        if not autopep8.check_syntax(code):
            raise SyntaxError("Tried to open file {} with invalid syntax".format(root))
        code = autopep8.fix_code(code)
        rootNode = ModuleNode(root.name[:-3], parent)
        scope = ScopeHandler()
        for line in code.splitlines():
            if len(line) == 0 or line.lstrip()[0] == "#":
                continue
            if not scope.isMain():
                if scope.addLine(line):
                    continue
                popScope(scope, rootNode)
            # Function
            match = re.fullmatch(FunctionNode.evaluateRegex, line)
            if match is not None:
                func = Function.parse(match.group(1), FuncType.GLOBAL, match.group(2), match.group(3))
                scope.push(func)
                continue
            # Class
            match = re.fullmatch(ClassNode.evaluateRegex, line)
            if match is not None:
                cls = Class.parse(match.group(1), match.group(2))
                scope.push(cls)
                continue
            # Variable
            match = re.fullmatch(VariableNode.evaluateRegex, line)
            if match is not None:
                try:
                    rootNode.find([rootNode.name, match.group(1)])
                except ValueError:
                    var = Variable(match.group(1), VarScope.MAIN, VarType.findFromStr(match.group(2)), match.group(3))
                    self.addElement(rootNode, VariableNode(var, rootNode))
            scope.addLine(line)
        while not scope.isMain():
            popScope(scope, rootNode)
        rootNode.mainFunc = scope.pop()
        return rootNode

    def crawlFunction(self, func: Function, parent: BaseNode):
        rootNode = FunctionNode(func, parent)
        for arg in func.args:
            self.addElement(rootNode, VariableNode(arg, rootNode))
        for line in func.code.splitlines():
            if len(line) == 0 or line.lstrip()[0] == "#":
                continue
            # Local variable
            match = re.fullmatch(VariableNode.evaluateRegex, line)
            if match is not None:
                try:
                    rootNode.find([rootNode.name, match.group(1)])
                except ValueError:
                    var = Variable(match.group(1), VarScope.FUNCTION, VarType.findFromStr(match.group(2)), match.group(3))
                    self.addElement(rootNode, VariableNode(var, rootNode))
        return rootNode

    def crawlClass(self, cls: Class, parent: BaseNode):
        def popScope(scope: ScopeHandler, rootNode):
            elem = scope.pop()
            if isinstance(elem, Function):
                elem = self.crawlClassFunc(elem, rootNode)
            self.addElement(rootNode, elem)

        rootNode = ClassNode(cls, parent)
        scope = ScopeHandler()
        isNextStatic = False
        for line in cls.code.splitlines():
            if len(line) == 0 or line.lstrip()[0] == "#":
                continue
            if not scope.isMain():
                if scope.addLine(line):
                    continue
                popScope(scope, rootNode)
            # Check if method is static
            match = re.fullmatch(r"\s*@staticmethod", line)
            if match is not None:
                isNextStatic = True
                continue
            # Function
            match = re.fullmatch(FunctionNode.objEvaluateRegex, line)
            if match is not None:
                if match.group(2) is None and not isNextStatic:
                    raise SyntaxError("Tried to define non-static method without self argument")
                funcType = FuncType.METHOD if not isNextStatic else FuncType.STATICMETHOD
                func = Function.parse(match.group(1), funcType, match.group(3), match.group(4))
                scope.push(func)
                continue
            isNextStatic = False
            # Variable
            match = re.fullmatch(VariableNode.evaluateRegex, line)
            if match is not None:
                try:
                    rootNode.find([rootNode.name, match.group(1)])
                except ValueError:
                    var = Variable(match.group(1), VarScope.CLASS, VarType.findFromStr(match.group(2)), match.group(3))
                    self.addElement(rootNode, VariableNode(var, rootNode))
        while not scope.isMain():
            popScope(scope, rootNode)
        return rootNode

    def crawlClassFunc(self, func: Function, parent: BaseNode):
        rootNode = FunctionNode(func, parent)
        for arg in func.args:
            self.addElement(rootNode, VariableNode(arg, rootNode))
        for line in func.code.splitlines():
            if len(line) == 0 or line.lstrip()[0] == "#":
                continue
            # Local variable
            match = re.fullmatch(VariableNode.evaluateRegex, line)
            if match is not None:
                try:
                    rootNode.find([rootNode.name, match.group(1)])
                except ValueError:
                    var = Variable(match.group(1), VarScope.FUNCTION, VarType.findFromStr(match.group(2)), match.group(3))
                    self.addElement(rootNode, VariableNode(var, rootNode))
            # Class variable
            match = re.fullmatch(VariableNode.objEvaluateRegex, line)
            if match is not None:
                try:
                    rootNode.parent.find([rootNode.parent.name, match.group(1)])
                except ValueError:
                    var = Variable(match.group(1), VarScope.OBJECT, VarType.findFromStr(match.group(2)), match.group(3))
                    self.addElement(rootNode.parent, VariableNode(var, rootNode.parent))
        return rootNode

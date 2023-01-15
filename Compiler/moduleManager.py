import os
import re
import autopep8
from pathlib import Path

from Compiler.classManager import ClassManager
from Compiler.codeManager import CodeManager
from Compiler.functionManager import FunctionManager
from Compiler.variableManager import VariableManager, VariableData


class ModuleInstance:
    class ImportManager:
        def __init__(self, compiler):
            from Compiler.compiler import Compiler
            self.compiler: Compiler = compiler

            self.importEntries: dict[str: [str]] = {}
            self.imports: list[str] = []

        def addImportEntry(self, importPath: str, elemList: list[str] = None):
            elemList = elemList if elemList is not None else []
            if importPath in self.importEntries:
                return
            self.importEntries[importPath] = elemList

        def addImport(self, importName: str):
            if importName in self.imports:
                return
            self.imports.append(importName)

        def processImports(self) -> list[tuple[str, str]]:
            substitutions: list[tuple[str, str]] = []
            for elem, targets in self.importEntries.items():
                module = self.compiler.moduleManager.isModule(elem)
                if module is not None:
                    self.addImport(module)
                for target in targets:
                    fullTarget = (module if module is not None else elem) + "." + target
                    if self.compiler.moduleManager.isModule(fullTarget):
                        self.addImport(fullTarget)
                    substitutions.append((target, fullTarget))
            self.importEntries.clear()
            return substitutions

        def getImports(self) -> list[str]:
            return self.imports

    def __init__(self, target: str, compiler):
        from Compiler.compiler import Compiler
        self.compiler: Compiler = compiler

        self.importName = target.replace("\\", ".")
        self.targetName = os.path.join("files", "input", target + ".py")
        with open(self.targetName, "r") as inputFile:
            code = inputFile.read()
            if not autopep8.check_syntax(code):
                raise SyntaxError("Tried to open file {} with invalid syntax".format(self.targetName))
            self.inputCode: str = autopep8.fix_code(code)

        self.importManager = ModuleInstance.ImportManager(compiler)

    def parseImports(self):
        fromImportMatch = re.findall("(?:\n|^)from ([\w.]+) import ((?:[\w*]+(?:, )?)+)", self.inputCode)
        for match in fromImportMatch:
            if "*" in match[1]:
                raise SyntaxError("This compiler does not support '*' imports!!")
            targets: list[str] = match[1].split(", ")
            self.importManager.addImportEntry(match[0], targets)
            self.inputCode = self.inputCode.replace("from " + match[0] + " import " + match[1] + "\n", "")

        importMatch = re.findall("(?:\n|^)import (\w+)", self.inputCode)
        for match in importMatch:
            self.importManager.addImportEntry(match)
            self.inputCode = self.inputCode.replace("import " + match + "\n", "")

        for target, fullTarget in self.importManager.processImports():
            matches = re.findall("([^.])((?:\w+\.)*" + target + ")", self.inputCode)
            for match in matches:
                self.inputCode = self.inputCode.replace(match[0] + match[1], match[0] + fullTarget)

        for importFile in self.importManager.getImports():
            route = importFile.split(".")
            importFile = os.path.join(*route)
            self.compiler.moduleManager.addImportedFile(importFile)

    def deaimguateDeclarations(self):
        newCode = []
        for line in list(filter(lambda x: x != "", self.inputCode.split("\n"))):
            matchVars: list[VariableData] = VariableManager.parse(line)
            if len(matchVars) > 0:
                line = ""
                for var in matchVars:
                    if "." in var.name:
                        var.name = var.name.replace(".", "_")
                    else:
                        var.name = self.importName.replace(".", "_") + "_" + var.name
                    if var.type is not None:
                        var.type = (": " + var.type.value)
                    else:
                        var.type = ""
                    if var.extraData is not None:
                        var.type = var.type.replace("%meta%", var.extraData)
                    line += var.name + var.type + " " + var.assignmentType + " " + var.value + "\n"
                line = line.rstrip()
            match: re.Match = re.search("([\w.]+)\.([\w\d]+)", line)
            if match is not None:
                if match.group(1) in self.importManager.imports:
                    line = line.replace(match.group(0), match.group(0).replace(".", "_"))
            match: re.Match = FunctionManager.parse(line)
            if match is not None:
                line = line.replace(match.group(1), self.importName.replace(".", "_") + "_" + match.group(1))
            match: re.Match = ClassManager.parse(line)
            if match is not None:
                line = line.replace(match.group(1), self.importName.replace(".", "_") + "_" + match.group(1))
            newCode.append(line)
        self.inputCode = "\n".join(newCode)


class ModuleManager:
    def __init__(self, compiler):
        from Compiler.compiler import Compiler
        self.compiler: Compiler = compiler
        self.foundModules: [str] = []
        self.imports: dict[str: ModuleInstance] = {}
        self.root: str = None

    def sweepFiles(self):
        self.foundModules = [elem.as_posix().replace("files/input/", "").replace("/", ".")[:-3] for elem in list(Path("files/input").rglob("*.py"))]

    def setRoot(self, root: str):
        self.root = root

    def isModule(self, symbol: str) -> str | None:
        if symbol in self.foundModules:
            return symbol
        for elem in self.foundModules:
            match = re.compile("(.)*" + symbol + "$").match(elem)
            if match is not None:
                return elem
        return None

    def addImportedFile(self, importName: str) -> str:
        newName = Path(importName).as_posix().replace("/", ".")
        if newName in self.imports:
            return newName
        codeManager = ModuleInstance(importName, self.compiler)
        self.imports[newName] = codeManager
        codeManager.parseImports()
        return newName

    def findRecursiveImports(self, moduleName: str) -> list[str]:
        module: ModuleInstance = self.imports[moduleName]
        importList = []
        for importElem in module.importManager.getImports():
            if importElem not in importList:
                for elem in self.findRecursiveImports(importElem):
                    if elem not in importList:
                        importList.append(elem)
                importList.append(importElem)
        return importList

    def mergeImports(self) -> CodeManager:
        if self.root not in self.imports:
            raise AttributeError("Tried to merge imports into non-existing root module. Did you set the correct root module?")
        imports = self.findRecursiveImports(self.root)
        imports.append(self.root)
        codeManager = CodeManager()
        for importElem in imports:
            imp: ModuleInstance = self.imports[importElem]
            imp.deaimguateDeclarations()
            codeManager.addCodeBack(importElem, imp.inputCode)
        return codeManager

from Compiler.moduleManager import ModuleManager


class Compiler:
    def __init__(self, target: str):
        self.initialTarget = target
        self.moduleManager: ModuleManager = ModuleManager(self)
        self.codeManager = None

    def compile(self):
        self.moduleManager.sweepFiles()
        module = self.moduleManager.addImportedFile(self.initialTarget)
        self.moduleManager.setRoot(module)
        self.codeManager = self.moduleManager.mergeImports()
        self.codeManager.gatherSymbols()
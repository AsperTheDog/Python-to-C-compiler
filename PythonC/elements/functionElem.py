import re
from enum import Enum

from PythonC.elements.variableElem import Variable, VarType, VarScope


class FuncType(Enum):
    GLOBAL = 0
    METHOD = 1
    STATICMETHOD = 2


class Function:
    def __init__(self, name: str, funcType: FuncType, args: list[Variable], ret: VarType):
        self.name = name
        self.args = args
        self.ret = ret
        self.code = ""
        self.type = funcType

    def addCode(self, lines: list[str]):
        self.code = "\n".join(lines)

    @staticmethod
    def parse(name: str, funcType: FuncType, args: str, ret: str):
        args = args.lstrip(", ").split(", ") if args != "" else []
        parsedArgs = []
        for arg in args:
            match = re.fullmatch(r"([\w\d]+)(?:: ([\w]+))?(?: = (.+))?", arg)
            if match is None:
                raise SyntaxError("Invalid syntax for function argument. This should never happen, if this triggered the regex is wrong")
            parsedArgs.append(Variable(match.group(1), VarScope.FUNCTION, VarType.findFromStr(match.group(2)), match.group(3)))
        ret = VarType.findFromStr(ret)
        return Function(name, funcType, parsedArgs, ret)

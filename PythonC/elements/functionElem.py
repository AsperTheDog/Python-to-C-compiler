import re
from PythonC.elements.variableElem import Variable, VarType


class Function:
    def __init__(self, name: str, args: list[Variable], ret: VarType):
        self.name = name
        self.args = args
        self.ret = ret
        self.code = ""

    def addCode(self, lines: list[str]):
        self.code = "\n".join(lines)

    @staticmethod
    def parse(name: str, args: str, ret: str):
        args = args.split(", ") if args != "" else []
        parsedArgs = []
        for arg in args:
            match = re.fullmatch(r"([\w\d]+)(?:: ([\w]+))?(?: = (.+))?", arg)
            if match is None:
                raise SyntaxError("Invalid syntax for function argument. This should never happen, if this triggered the regex is wrong")
            parsedArgs.append(Variable(match.group(1), VarType.findFromStr(match.group(2)), match.group(3)))
        ret = VarType.findFromStr(ret)
        return Function(name, parsedArgs, ret)
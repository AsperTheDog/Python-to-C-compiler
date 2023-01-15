import re


class FunctionManager:
    def __init__(self):
        self.functions = {}

    @staticmethod
    def parse(snippet: str) -> re.Match:
        return re.match("def ([\w\d]+)\(((?:[\w\d.]+: \w+(?:, )?)*)\):", snippet)

    def add(self, name: str, args: str, lines: list[str]):
        self.functions[name] = (args, lines)
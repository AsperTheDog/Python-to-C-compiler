import re


class ExpressionParser:
    def __init__(self):
        pass

    @classmethod
    def divideExpressions(cls, snippet: str, expectedNum: int):
        match = re.match("\((.+)\)", snippet)
        if match is not None:
            snippet = match.group(1)
        stack = 0
        begin = 0
        expressions = []
        for end, elem in enumerate(snippet):
            if elem == '(' or elem == '[' or elem == '{':
                stack += 1
            elif elem == ')' or elem == ']' or elem == '}':
                stack -= 1
            if stack == 0 and elem == ',':
                expressions.append(snippet[begin:end].strip())
                begin = end + 1
        expressions.append(snippet[begin:].strip())
        return list(filter(lambda x: x != "", expressions))

    @staticmethod
    def processComment(line):
        scope = False
        count = 0
        for char in line:
            if char == '"':
                scope = not scope
                continue
            if not scope and char == "#":
                return line[count:]
        return ""

    @classmethod
    def parse(cls, snippet: str):
        pass
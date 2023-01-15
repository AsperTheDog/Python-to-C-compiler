import re


class ClassManager:
    def __init__(self):
        self.classes = {}

    def add(self, name: str, parents: str, lines: list[str]):
        self.classes[name] = (parents, lines)

    def doesClassExist(self, className):
        return className in self.classes

    @staticmethod
    def parse(snippet: str):
        return re.match("class ([\w\d]+)(?:\(([\w\d,. ]+)\))?:", snippet)
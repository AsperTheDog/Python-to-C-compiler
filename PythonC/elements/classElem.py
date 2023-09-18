

class Class:
    def __init__(self, name: str, parents: list[str]) -> None:
        self.name = name
        self.parents = parents
        self.code = None

    def addCode(self, lines: list[str]):
        self.code = "\n".join(lines)

    @staticmethod
    def parse(name: str, parents: str):
        parents = parents.split(", ") if parents else None
        return Class(name, parents)

import a_model as am


class AbstractSyntaxTree:
    def __init__(self, root: am.ParserNode):
        self.root = root

    def __str__(self):
        return str(self.root)

    def __repr__(self):
        return str(self)

    def eval(self):
        return self.root.eval()

    def find(self, name):
        return self.root.find(name)

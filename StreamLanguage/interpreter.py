class Interpretor:
    def __init__(self):
        self.vars = {}
        self.stack = []
        self.output = ""
        self.functions = {}
        self.scope = []
        self.current_function = None
        self.current_function_name = None
        self.current_function_args = None

    def run(self, ast: tuple):
        for node in ast:
            self.visit(node)

    def visit(self, node: tuple):
        type = node[0]
        match type:
            case "function_definition":
                self.visit_function_definition(node)
            case "function_call":
                self.visit_function_call(node)
            case "declaration":
                self.visit_declaration(node)
            case "if":
                self.visit_if(node)

    def visit_function_definition(self, node: tuple):
        name = node[1]
        args = node[2]
        body = node[3]
        self.functions[name] = (args, body)

    def visit_function_call(self, node: tuple):
        name = node[1]
        args = node[2]
        self.scope.append(self.vars)
        self.vars = {}
        self.current_function = self.functions[name]
        self.current_function_name = name
        self.current_function_args = args
        for i, arg in enumerate(args):
            self.vars[self.current_function[0][i]] = self.visit(arg)
        self.run(self.current_function[1])
        self.vars = self.scope.pop()
        self.output = self.vars.get("return", "")

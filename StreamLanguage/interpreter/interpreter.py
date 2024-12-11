from StreamLanguage.interpreter.contextN import Context
from StreamLanguage.parser.parser import Parser


class Interpreter:

    def __init__(self):
        self._parser = Parser()
        self._global_context = Context()
        self._global_context.register_builtin_functions()

    def interpret(self, text):
        tree = self._parser.parse(text)
        return tree.evaluate(self._global_context)

    def get_context(self):
        return self._global_context

    def set_context(self, context):
        self._global_context = context
        return self._global_context

    def get_parser(self):
        return self._parser

    def set_parser(self, parser):
        self._parser = parser
        return self._parser

    def __str__(self):
        return "Interpreter"
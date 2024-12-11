# This file is the main file for the interpreter
from StreamLanguage.interpreter.interpreter import Interpreter


def main_test():
    with open("guess.sl", "r") as file:
        text = file.read()

    interpreter = Interpreter()
    result = interpreter.interpret(text)

    print(result)


if __name__ == "__main__":
    main_test()

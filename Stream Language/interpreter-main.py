from parser import parse
from interpreter import Interpretor

def main():
    with open("test.sl", "r") as f:
        code = f.read()
    ast = parse(code)
    interpretor = Interpretor()
    interpretor.run(ast)
    print(interpretor.output)


if __name__ == "__main__":
    main()
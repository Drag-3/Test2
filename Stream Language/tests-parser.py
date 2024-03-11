# Sample strings to test with parser
from parser import parse

tests = [
    """
    // This is a comment
    """,
    """
    /* This is also a comment
    But it is a multiline comment */
    """,
    """
    var x: int = 5;
    """,
    """
    var y = 6;
    """,
    """
    const z = x + y;
    """,
    """
    if (z > 10) {
        z = z + 20;
    }
    """,
    """
    if (z > 10) {
        z = z + 20;
    } else {
        z = z + 10;
    }
    """,
    """
    fn main() {
        var x: int = 5;
        var y = 6;
        var z = x + y;
        if (z > 10) {
            return true; // Return should only be used in functions
        }
    }
    """,
]


def build_tree(result: tuple[tuple[tuple[..., ...], ...], ...]):
    if result:
        if isinstance(result, tuple):
            for x in result:
                build_tree(x)
        else:
            print(result)


# Run the parser on the test cases
for x, test in enumerate(tests):
    result = parse(test)
    print(f"Test {x}")
    print(test)
    build_tree(result)

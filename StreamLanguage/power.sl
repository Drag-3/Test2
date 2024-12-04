// Program to calculate a number raised to a power using recursion
fn power(base: int, exponent: int) : int {
    if (exponent == 0) {
        return 1;
    } else {
        return base * power(base, exponent - 1);
    }
}

fn main() {
    var base: int = 3;
    var exponent: int = 4;
    var result: int = power(base, exponent);
    print(base + " raised to the power of " + exponent + " is " + result);
}

main();

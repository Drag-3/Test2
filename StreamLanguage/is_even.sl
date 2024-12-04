// Program to check if a number is even or odd
fn is_even(n: int) : boolean {
    if (n % 2 == 0) {  // mod needs precedence change
        return true;  // broken if statement is triggered correctly but fuunction returns false?
    } else {
        return false;
    }
}

fn main() {
    print("Enter a number to check if it is even or odd:");
    var number: int = read_int();
    if (is_even(number)) {
        print(number + " is even.");
    } else {
        print(number + " is odd.");
    }
}

main();

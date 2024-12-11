// Program to calculate the nth Fibonacci number using recursion

fn fibonacci(n){
        if (n <= 1) {
            return n;
        } else {
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
    }

fn main() {

    var position = 100; // Change this value to calculate a different Fibonacci number
    var fib_number = fibonacci(position);
    print("Fibonacci number at position " + position + " is " + fib_number);
}

main();

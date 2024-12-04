// Program for a guessing game
fn main() {
    var secret: int = 7; // Secret number to guess
    var guess: int = 0;

    print("Guess the secret number between 1 and 10.");

    while (guess != secret) {
        print("Enter your guess:");
        guess = read_int(); // Assuming read_int() reads an integer from user input

        if (guess < secret) {
            print("Too low!");
        } else {
            if (guess > secret) {
                print("Too high!");
            } else {
                print("Congratulations! You guessed it right.");
            }
        }
    }
}

main();

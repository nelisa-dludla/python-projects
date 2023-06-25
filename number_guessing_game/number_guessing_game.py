import random

print("===== Let's play the Number Guessing Game =====")
print(
    """
How to play:
1. The game will randomly select a number between 1 and 10.
2. Your goal is to guess the correct number.
3. After each guess, you will receive feedback on whether your guess was too high or too low.
4. You have three attempts to find the correct number.
5. Enjoy the thrill of the game and good luck!
"""
)

# Boolean to help continue or exit the game
repeat = True
while repeat:
    # Generate random number between 1 and 10
    generated_number = random.randint(1, 10)
    # Number of attempts the user has before it is game over
    attempts = 3
    # Boolean to help exit while loop when user wins
    winner = False
    while attempts != 0 and not winner:
        try:
            # Users guess
            user_guess = int(input("\nGuess: "))
        except ValueError:
            # Error message printed if user inputs anything other than a number/integer
            print("Invalid input. Please enter a number.")
        else:
            if user_guess > generated_number:
                attempts -= 1
                print(":| Too high")
            elif user_guess < generated_number:
                attempts -= 1
                print(":| Too low")
            else:
                print(":) You win")
                winner = True

    if attempts == 0:
        print(":( You lose")

    print("\nDo you want to play again?")

    # Boolean value to help determine if user has entered valid input
    valid_input = False
    while not valid_input:
        answer = input("Enter (y) for yes or (n) for no: ").lower()
        if answer == "n":
            print("Closing Number Guessing Game...")
            repeat = False
            valid_input = True
        # Error message printed if user enters anything other than y/n
        elif answer != "y":
            print("Invalid input")
        else:
            valid_input = True

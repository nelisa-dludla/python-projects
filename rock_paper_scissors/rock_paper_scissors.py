import random
import sys


def main():
    # Heading and Rules
    print("""===== Let's play Rock, Paper, Scissors! =====

How to Play

1. At the start of each round, you will be prompted to choose your move: rock, paper, or scissors.
2. The PC will randomly select its move.
3. The winner of the round will be determined based on the following rules:
    - Rock beats scissors
    - Scissors beat paper
    - Paper beats rock
4. The game will display the winner of each round and keep track of the overall score.
5. Enjoy the game and aim for victory!
    """)

    player_score = 0
    pc_score = 0
    game_round = 0
    # Main game loop
    while True:
        # Valid options for the user to choose
        game_choices = ["r", "p", "s"]
        # PC's choice
        pc_choice = random.choice(game_choices)
        game_round += 1
        # Print current game round and score
        print(f"""\n===== Round {game_round} =====
              \nPlayer: {player_score}\nPC: {pc_score}
              """)
        # Loop helps re-prompt the user should they enter an invalid option
        correct_choice = False
        while not correct_choice:
            # User input
            player_choice = (
                input("\nPick (r) for rock, (p) for paper and (s) for scissors: ")
                .strip()
                .lower()
            )
            if player_choice not in game_choices:
                print("Invalid input.")
            elif player_choice == pc_choice:
                print("It's a draw!")
                break
            elif (
                player_choice == "r"
                and pc_choice == "p"
                or player_choice == "p"
                and pc_choice == "s"
                or player_choice == "s"
                and pc_choice == "r"
            ):
                print("PC wins this round!")
                pc_score += 1
                break
            else:
                print("You win!")
                player_score += 1
                break
        # Loop helps re-prompt the user should they enter an invalid option
        play_again = False
        while not play_again:
            response = (
                input(
                    "\nWould you like to play again?\nPick (y) for yes or (n) for no: "
                )
                .strip()
                .lower()
            )
            response_choices = ["y", "n"]

            if response not in response_choices:
                print("Invalid input.")
            elif response == "y":
                play_again = True
            else:
                print(f"""\n=== Final Score ===
Player: {player_score}\nPC: {pc_score}
                """)
                sys.exit("\nClosing Rock, Paper, Scissors...")


if __name__ == "__main__":
    main()

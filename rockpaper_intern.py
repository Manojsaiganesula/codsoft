import random
import os

# Keep track of wins and losses
player_wins = 0
computer_wins = 0
ties = 0

def clear_screen():
    """Clear the screen to make it look cleaner"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_welcome_message():
    """Show a nice welcome message to the player"""
    print("=" * 50)
    print("    🎮 WELCOME TO ROCK PAPER SCISSORS! 🎮")
    print("=" * 50)
    print()
    print("Game Rules:")
    print("🪨 Rock beats Scissors")
    print("✂️  Scissors beats Paper") 
    print("📄 Paper beats Rock")
    print()

def get_player_choice():
    """Ask the player what they want to choose"""
    print("What's your choice?")
    print("1 - Rock 🪨")
    print("2 - Paper 📄")
    print("3 - Scissors ✂️")
    print()
    
    while True:
        try:
            choice = input("Enter 1, 2, or 3 (or 'quit' to exit): ").strip().lower()
            
            # Let player quit anytime
            if choice == 'quit' or choice == 'q':
                return 'quit'
            
            # Convert number to choice
            if choice == '1':
                return 'rock'
            elif choice == '2':
                return 'paper'
            elif choice == '3':
                return 'scissors'
            # Also accept direct words
            elif choice in ['rock', 'paper', 'scissors']:
                return choice
            else:
                print("Please enter 1, 2, 3, or type the choice directly!")
                
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            return 'quit'

def get_computer_choice():
    """Computer picks randomly"""
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def show_choices(player_choice, computer_choice):
    """Show what both player and computer chose"""
    choice_emojis = {
        'rock': '🪨',
        'paper': '📄', 
        'scissors': '✂️'
    }
    
    print("-" * 30)
    print(f"You chose: {choice_emojis[player_choice]} {player_choice.title()}")
    print(f"Computer chose: {choice_emojis[computer_choice]} {computer_choice.title()}")
    print("-" * 30)

def determine_winner(player_choice, computer_choice):
    """Figure out who won the game"""
    # Check for tie first
    if player_choice == computer_choice:
        return 'tie'
    
    # Check all the ways player can win
    winning_combinations = {
        'rock': 'scissors',      # rock beats scissors
        'scissors': 'paper',     # scissors beats paper
        'paper': 'rock'          # paper beats rock
    }
    
    if winning_combinations[player_choice] == computer_choice:
        return 'player'
    else:
        return 'computer'

def show_result(winner, player_choice, computer_choice):
    """Show who won and update the score"""
    global player_wins, computer_wins, ties
    
    if winner == 'tie':
        print("🤝 It's a tie! Great minds think alike!")
        ties += 1
    elif winner == 'player':
        print("🎉 You WIN! Awesome!")
        # Explain why they won
        explanations = {
            ('rock', 'scissors'): "Rock crushes Scissors!",
            ('scissors', 'paper'): "Scissors cuts Paper!",
            ('paper', 'rock'): "Paper covers Rock!"
        }
        explanation = explanations.get((player_choice, computer_choice), "")
        if explanation:
            print(f"💪 {explanation}")
        player_wins += 1
    else:
        print("😔 Computer wins this round!")
        # Explain why computer won
        explanations = {
            ('rock', 'scissors'): "Rock crushes Scissors!",
            ('scissors', 'paper'): "Scissors cuts Paper!",
            ('paper', 'rock'): "Paper covers Rock!"
        }
        explanation = explanations.get((computer_choice, player_choice), "")
        if explanation:
            print(f"🤖 {explanation}")
        computer_wins += 1
    
    print()

def show_current_score():
    """Display the current score"""
    total_games = player_wins + computer_wins + ties
    
    print("📊 CURRENT SCORE:")
    print(f"   You: {player_wins} wins")
    print(f"   Computer: {computer_wins} wins") 
    print(f"   Ties: {ties}")
    print(f"   Total games: {total_games}")
    
    # Show win percentage if they played games
    if total_games > 0:
        win_percentage = (player_wins / total_games) * 100
        print(f"   Your win rate: {win_percentage:.1f}%")
    
    print()

def ask_play_again():
    """Ask if the player wants to play another round"""
    while True:
        choice = input("Do you want to play again? (yes/no): ").strip().lower()
        if choice in ['yes', 'y', 'yeah', 'yep']:
            return True
        elif choice in ['no', 'n', 'nope']:
            return False
        else:
            print("Please answer yes or no!")

def show_final_stats():
    """Show final statistics when game ends"""
    total_games = player_wins + computer_wins + ties
    
    if total_games == 0:
        print("No games played. Thanks for checking out the game!")
        return
    
    print("🏁 FINAL GAME STATISTICS:")
    print("=" * 40)
    print(f"Total games played: {total_games}")
    print(f"Your wins: {player_wins}")
    print(f"Computer wins: {computer_wins}")
    print(f"Ties: {ties}")
    
    win_percentage = (player_wins / total_games) * 100
    print(f"Your final win rate: {win_percentage:.1f}%")
    
    # Give them a nice message based on performance
    if win_percentage >= 70:
        print("🏆 AMAZING! You're a Rock Paper Scissors champion!")
    elif win_percentage >= 50:
        print("👍 Great job! You held your own against the computer!")
    elif win_percentage >= 30:
        print("😊 Not bad! Practice makes perfect!")
    else:
        print("🎮 Thanks for playing! Better luck next time!")
    
    print("=" * 40)

def main():
    """Main game function - this runs everything"""
    print("Starting Rock Paper Scissors Game...")
    
    # Show welcome message
    clear_screen()
    show_welcome_message()
    
    # Keep playing until player wants to quit
    while True:
        # Get what the player wants to choose
        player_choice = get_player_choice()
        
        # If they want to quit, break out of the loop
        if player_choice == 'quit':
            break
        
        # Get computer's choice
        computer_choice = get_computer_choice()
        
        # Show both choices
        show_choices(player_choice, computer_choice)
        
        # Figure out who won
        winner = determine_winner(player_choice, computer_choice)
        
        # Show the result
        show_result(winner, player_choice, computer_choice)
        
        # Show current score
        show_current_score()
        
        # Ask if they want to play again
        if not ask_play_again():
            break
        
        print()  # Add some space before next round
    
    # Game is over, show final stats
    clear_screen()
    show_final_stats()
    print("\nThanks for playing Rock Paper Scissors! 👋")

# This is where the program starts
if __name__ == "__main__":
    main()
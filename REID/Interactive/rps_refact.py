# Ask the user to make a choice
#If choice is not valid
# print error
# let comp make a choice
# print choices (emojis)
#Determine the winner
# Ask the user if they want to continue
# If not
#Terminate

#windows key and period

import random
# Dictionary is used to map a key to a value
 
emojis = {'r':'🌚', 's':'✂','p':'🧻'}
choices = ('r','p','s')

def get_user_choice():
    while True:
        user_choice = input('Rock, paper or scissor? (r/p/s): ').lower()
        if user_choice in choices: # changes this to if the state IS true
            return user_choice
        else:
            print('Invalid choice!') # don't need the continue because this error moves back to while loop

def display_choices(user_choice, computer_choice): #since user_choice and computer_choice are not yet defined, add them as variables as arguements where ever referenced
    print(f'You chose {emojis[user_choice]}')
    print(f'Computer chose {emojis[computer_choice]}')

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        print('Tie')
    elif (
        (user_choice == 'r' and computer_choice == 's') or 
        (user_choice == 's' and computer_choice == 'p') or 
        (user_choice == 'p' and computer_choice == 'r')):
        print('You win')
    else:
        print('You lose')


def play_game():
    while True:
        user_choice = get_user_choice() # store the result of the get_user_choice function inside of a variable user_choice

        computer_choice = random.choice(choices)

        display_choices(user_choice, computer_choice)

        determine_winner(user_choice, computer_choice)

        should_continue = input('Continue? (y/n): ').lower()
        if should_continue == 'n':
            break

play_game() # since the refactoring all of the functionality has been nested into other defs therefore the game doesn't start without calling the function last
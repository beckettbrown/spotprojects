
#basic gameloop mechanics for guessing handler
import random

#direction choices

directions = ['left', 'foward', 'right']

def jarvis_choice(): #Jarvis access the random import to select a direction
    return random.choice(directions)

def player_choice():    #Player choice handler
    print("Choose a direction: left, foward, right.") # instruction direction prompt
    choice = input("Enter your choice: ") #Input request
    if choice in directions: #If the player selects one of the three
        return choice
    else:
        print("Invalid Choice. Try Again.")
        return player_choice()
    
def determine_winner(player_choice, jarvic_choice):
    print(f"Player choice: {player_choice}")
    print(f"Jarvis choice: {jarvis_choice}")

    if player_choice == jarvis_guess:
        return "celebrate"
    else:
        return "pout"
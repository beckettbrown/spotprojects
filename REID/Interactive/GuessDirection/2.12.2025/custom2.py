#GAME
#Imports
import random

#dictionaries
play_choices = ('y','n')
choices = ('left','forward','right') #dictionary of acceptable inputs from user_choice


while True: #creates a loop to read through code
#Ask to Play Interactable: "Would you like to play?"
# JARVIS STANDS (POWER ON)

    play_game = input('Would you like to play with me? (y/n): ').lower() #asks for input for players and converts input to lowercase
    if play_game not in play_choices:
        print('Im not sure what that means. Do you want to play?') # Invalid choice response
        continue #restart requesting
    if play_game == 'y': #if the play_game returns y 
        print('Lets play!') #prints lets play and loops again
 #IF YES ARM LIFT



#Jarvis and Game Script
        while True:
            user_choice = input('left, forward, right?:  ').lower() #asks the user for input and converts all answers to lowercase
            if user_choice not in choices: #If the user inputs something other than 'choice' options
                print('Invalid choice!') #Output invalid
                continue # jumps back to beginning of loop

            jarvis_choice = random.choice(choices) # Here jarvis' choice will randomly pull from 'choices' dictionary

    #Jarvis guesses a random direction
    #Player guesses a direction

            print(f'You guessed {user_choice}') #Prints out a prompt and users choice
            print(f'Jarvis guessed {jarvis_choice}') #Prints randomly selected jarvis choice

    #Compare directions
            if user_choice == jarvis_choice: # if the user and jarvis matches Jarvis wins
                print('I found you! I win!') #jarvis responds
                # JARVIS HAPPY DANCE
            else:
                print("Where'd you go? You win! ") #jarvis responses
                #JARVIS SAD DANCE
            
            play_game = input('Play again? (y/n): ').lower()
            if play_game not in play_choices:
                    print('Im not sure what that means. Do you want to play? (y/n):  ')
                    continue
            if play_game == 'n':
                    break

#IF NO JARVIS SITS (POWER OFF)

    else:  # if play_game returns n
        print('Goodnight! ZZzzz') #Prints a message on exit
        break #It breaks the loop and exits the code

    #If no
        #jarvis sits (power off)


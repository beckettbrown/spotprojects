
user_input = input("How many parts: ") # User is prompted to input number
if user_input is not int: #if the input is not an integer
    print("Invalid entry!") #print message
    
parts = int(user_input) #place the user's input and code it as an integer and place it under 'parts' object

def rotation_parts(parts): #take the 'parts' and place it into the rotation parts def
    return 360 / parts # divide 360 by 'parts' (360 represents a full rotation hard coded so it never changes)

degree = rotation_parts(parts) # return the result as 'degree'
print(f"Degree of Rotation for {parts} parts: {degree}") # return message
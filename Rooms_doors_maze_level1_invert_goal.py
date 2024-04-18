from openai import OpenAI
import numpy as np
import sys

# Initialize the client
client = OpenAI()

#grids definition
# Define the compound data type: one bool, one float, and one string
# 'U10' means Unicode string of maximum length 10
dtype = [('bool', bool), ('float', float), ('string', 'U300')]

# Initialize a 3x3 array with the defined data type, filled with default values
grid = np.zeros((2, 3), dtype=dtype)

# Assigning values
grid[0, 0] = (False, 1, 'You are in room 1. To your left, there is door leading to room 4. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[0, 1] = (True, 2, 'You are in room 2. To your left, there is door leading to room 3. To your right there is a door leading to room 1. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[0, 2] = (False, 3, 'You are in room 3. To your right, there is door leading to room 5. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')

grid[1, 0] = (False, 4, 'You are in room 4. You have reached the goal. Well done!')
grid[1, 1] = (False, 5, 'You are in room 5, There is no new door. Where would you like to go next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[1, 2] = (False, 6, 'This room is not accessible, choose another number and answer only this number.')


# Initialize the conversation history

conversation_history = [
    {"role": "system", "content": "You will be navigating through rooms, each with doors to your left, right, back, or in front of you. These doors lead to other rooms. Starting from room 2, your objective is to reach a goal located in another room. At each step, I will describe which new doors are available to you."},
]

#Initialize position
current_square = grid[0,1]

with open('test_doors_level_1.txt', 'a') as f:
    while grid[1,0][0] == False:
        if (current_square[0] == False) or (current_square[1] == 2):
            user_message = current_square[2]
        else:
            user_message = f"You are in room  {current_square[1]}. You already know what are your possible options since you already been there. Where will you go ? Choose an accessible room. VERY IMPORTANT: Answer only the room number you choose and nothing else."
        conversation_history.append({"role": "user", "content": user_message})
        print(f"User message: {user_message}")
        f.write(f"User message: {user_message}\n")  # Write to the file

        # Make the API request with the updated conversation history
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=conversation_history
        )

        # Extract the model's response and update the conversation history
        model_response = completion.choices[0].message.content.strip()
        conversation_history.append({"role": "system", "content": model_response})

        print(f"Model's choice: {model_response}")
        f.write(f"Model's choice: {model_response}\n")  # Write to the file
            
        #Process the model's response
        if model_response.isdigit() and 1 <= int(model_response) <= 5:
            if model_response == '4':
                grid[1, 0] = (True, grid[1, 0][1], grid[1, 0][2])
                user_message = f"You are in room 4. You have reached the goal. Well done!"
                print(f"User message: {user_message}")
                f.write(f"User message: {user_message}\n")
            else:
                # Find the corresponding square in beginner_grid
                for i in range(2):
                    for j in range(3):
                        if (grid[i, j][1] == current_square[1]):
                            grid[i, j] = (True, grid[i, j][1], grid[i, j][2])
                            break

                for i in range(2):
                    for j in range(3):
                        if grid[i, j][1] == int(model_response):
                            current_square = grid[i, j]
                            break
        else:
            #intervention ext
            manual_user_message = input("INTERVENTION EXT: ")
            user_message = manual_user_message
            conversation_history.append({"role": "user", "content": user_message})

    
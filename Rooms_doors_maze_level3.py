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
grid = np.zeros((5, 5), dtype=dtype)

# Assigning values
grid[0, 0] = (False, 1, 'You are in room 1. There is no new door. Where would you like to go next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[0, 1] = (False, 2, 'You are in room 2. In front of you, there is door leading to room 1. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[0, 2] = (True, 3, 'You are in room 3. To your right, there is door leading to room 2. To your left, there is a door leading to room 4. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[0, 3] = (False, 4, 'You are in room 4. To your right, there is door leading to room 6. In front of you, there is a door leading to room 5. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[0, 4] = (False, 5, 'You are in room 5. To your right, there is door leading to room 7. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')

grid[1, 3] = (False, 6, 'You are in room 6. In front of you, there is door leading to room 11. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[1, 4] = (False, 7, 'You are in room 7. In front of you, there is door leading to room 12. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')

grid[2, 0] = (False, 8, 'You are in room 8. To your left, there is door leading to room 13. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[2, 1] = (False, 9, 'You are in room 9. In front of you, there is door leading to room 8. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[2, 2] = (False, 10, 'You are in room 10. In front of you, there is door leading to room 9. To your left, there is a door leading to room 14. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[2, 3] = (False, 11, 'You are in room 11. To your right, there is door leading to room 10. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[2, 4] = (False, 12, 'You are in room 12. There is no new door. Where would you like to go next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')

grid[3, 0] = (False, 13, 'You are in room 13. In front of you, there is door leading to room 15. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[3, 2] = (False, 14, 'You are in room 14. In front of you, there is door leading to room 16. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')

grid[4, 0] = (False, 15, 'You are in room 15. You reached the goal. Well done!')
grid[4, 2] = (False, 16, 'You are in room 16. To your left, there is door leading to room 17. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[4, 3] = (False, 17, 'You are in room 17. In front of you, there is door leading to room 18. Which room would you like to enter next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')
grid[4, 4] = (False, 18, 'You are in room 18. There is no new door. Where would you like to go next? VERY IMPORTANT: Answer only the room number you choose and nothing else.')

# Initialize the conversation history

conversation_history = [
    {"role": "system", "content": "You will be navigating through rooms, each with doors to your left, right, back, or in front of you. These doors lead to other rooms. Starting from room 3, your objective is to reach a goal located in another room. At each step, I will describe which new doors are available to you."},
]

#Initialize position
current_room = grid[0,2]

with open('test_doors_level_3.txt', 'a') as f:

    while grid[4,0][0] == False:
        if (current_room[0] == False) or (current_room[1] == 3):
            user_message = current_room[2]
        else:
            user_message = f"You are in room  {current_room[1]}. You already know what are your possible options since you already been there. Where will you go ? Choose an accessible room. VERY IMPORTANT: Answer only the room number you choose and nothing else."
        conversation_history.append({"role": "user", "content": user_message})
        print(f"User message: {user_message}")
        f.write(f"User message: {user_message}\n")  # Write to the file

        # Make the API request with the updated conversation history
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history
        )

        # Extract the model's response and update the conversation history
        model_response = completion.choices[0].message.content.strip()
        conversation_history.append({"role": "system", "content": model_response})

        print(f"Model's choice: {model_response}")
        f.write(f"Model's choice: {model_response}\n")  # Write to the file
            
        #Process the model's response
        if model_response.isdigit() and 1 <= int(model_response) <= 18:
            if model_response == '15':
                grid[4, 0] = (True, grid[4, 0][1], grid[4, 0][2])
                user_message = f"You are in room 15. You have reached the goal. Well done!"
                print(f"User message: {user_message}")
                f.write(f"User message: {user_message}\n")
            else:
                # Find the corresponding square in beginner_grid
                for i in range(5):
                    for j in range(5):
                        if (grid[i, j][1] == current_room[1]):
                            grid[i, j] = (True, grid[i, j][1], grid[i, j][2])
                            break

                for i in range(5):
                    for j in range(5):
                        if grid[i, j][1] == int(model_response):
                            current_room = grid[i, j]
                            break
        else:
            #intervention ext
            manual_user_message = input("INTERVENTION EXT: ")
            user_message = manual_user_message
            conversation_history.append({"role": "user", "content": user_message})

    if (grid[4,0][0] == True)and(grid[0,0][0] ==  True):
        user_message = f"You reached the goal, well done! Now imagine that when you entered room 1 there was a door on your left connecting the room to room 8, is there any other way to reach the exit? If yes, please provide the room sequence."
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history
        )
        conversation_history.append({"role": "user", "content": user_message})
        print(f"User message: {user_message}")
        f.write(f"User message: {user_message}\n")  # Write to the file


        # Extract the model's response and update the conversation history
        model_response = completion.choices[0].message.content.strip()
        conversation_history.append({"role": "system", "content": model_response})
        print(f"Model's choice: {model_response}")
        f.write(f"Model's choice: {model_response}\n")  # Write to the file
        
        while True:
            manual_user_message = input("INTERVENTION EXT: ")
            user_message = manual_user_message
            conversation_history.append({"role": "user", "content": user_message})
            print(f"User message: {user_message}")
            f.write(f"User message: {user_message}\n")  # Write to the file

            if user_message == 'STOP':
                f.close()
                exit()

            completion = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history
            )

            model_response = completion.choices[0].message.content.strip()
            conversation_history.append({"role": "system", "content": model_response})
            print(f"Model's choice: {model_response}")
            f.write(f"Model's choice: {model_response}\n")  # Write to the file

    if (grid[4,0][0] == True)and(grid[4,2][0] ==  True):
        user_message = f"You reached the goal, well done! Now imagine that when you entered room 16 for the first time, there was a door on your right connecting the room to room 15, is there any other way to reach the exit? If yes, please provide the room sequence."
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history
        )
        conversation_history.append({"role": "user", "content": user_message})
        print(f"User message: {user_message}")
        f.write(f"User message: {user_message}\n")  # Write to the file


        # Extract the model's response and update the conversation history
        model_response = completion.choices[0].message.content.strip()
        conversation_history.append({"role": "system", "content": model_response})
        print(f"Model's choice: {model_response}")
        f.write(f"Model's choice: {model_response}\n")  # Write to the file
        
        while True:
            manual_user_message = input("INTERVENTION EXT: ")
            user_message = manual_user_message
            conversation_history.append({"role": "user", "content": user_message})
            print(f"User message: {user_message}")
            f.write(f"User message: {user_message}\n")  # Write to the file

            if user_message == 'STOP':
                f.close()
                exit()

            completion = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history
            )

            model_response = completion.choices[0].message.content.strip()
            conversation_history.append({"role": "system", "content": model_response})
            print(f"Model's choice: {model_response}")
            f.write(f"Model's choice: {model_response}\n")  # Write to the file
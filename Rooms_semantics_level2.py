from openai import OpenAI
import numpy as np
import sys

# Initialize the client
client = OpenAI()

# grids definition
# Define the compound data type: one bool, one float, and one string
# 'U10' means Unicode string of maximum length 10
dtype = [('bool', bool), ('name', 'U20'), ('string', 'U300')]

# Initialize a 5x5 array with the defined data type, filled with default values
grid = np.zeros((5,5), dtype=dtype)

# Assigning values
grid[0, 0] = (False, 'Bedroom 1', 'You are in the "Bedroom 1". There is no new door. Where would you like to go next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[0, 1] = (False, 'Living room', 'You are in the "Living room". In front of you, there is door leading to the "Bedroom 1". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[0, 2] = (True, 'Entrance', 'You are in the "Entrance". To your right, there is door leading to the "Living room". To your left, there is a door leading to the "Garage". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[0, 3] = (False, 'Garage', 'You are in the "garage". To your right, there is door leading to the "Storage". In front of you, there is a door leading to the "Patio". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[0, 4] = (False, 'Patio', 'You are in the "Patio". To your right, there is door leading to the "Gym". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')

grid[1, 3] = (False, 'Storage', 'You are in the "Storage". In front of you, there is door leading to the "Laundry room". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[1, 4] = (False, 'Gym', 'You are in the "Gym". In front of you, there is door leading to the "Bathroom 3". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')

grid[2, 0] = (False, 'Dining room', 'You are in the "Dining room". To your left, there is door leading to the "Kitchen". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[2, 1] = (False, 'Living room 2', 'You are in the "Living room 2". In front of you, there is door leading to the "Dining room". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[2, 2] = (False, 'Library', 'You are in the "Library". In front of you, there is door leading to the "Living room 2". To your left, there is a door leading to the "Bedroom 2". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[2, 3] = (False, 'Laundry room', 'You are in the "Laundry room". To your right, there is door leading to the "Library". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[2, 4] = (False, "Bathroom 1", 'You are in the bathroom 1. There is no new door. Where would you like to go next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')

grid[3, 0] = (False, 'Kitchen', 'You are in the kitchen. There is no new door. Where would you like to go next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[3, 2] = (False, 'Bedroom 2', 'You are in the "Bedroom 2". In front of you, there is door leading to the Dressing room. Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')

grid[4, 2] = (False, "Dressing room", 'You are in the "Dressing room". To your left, there is door leading to the "Bathroom 2". Which room would you like to enter next? VERY IMPORTANT: Answer only the room name you choose and nothing else.')
grid[4, 3] = (False, "Bathroom 2", 'You are in the "Bathroom 2". You reached the goal, well done !')

# Initialize the conversation history

conversation_history = [
    {"role": "system", "content": "You will be in a house, and I will describe the other rooms you can directly access from your current location. Starting from the entrance hall, your task is to find my hair dryer"},
]

#Initialize position
current_room = grid[0,2]

with open('test_semantics_level_2.txt', 'a') as f:

    while grid[4,3][0] == False:
        if (current_room[0] == False) or (current_room[1] == 'Entrance'):
            user_message = current_room[2]
        else:
            user_message = f"You are in the  {current_room[1]}. You already know what are your possible options since you already been there. Where will you go ? Choose an accessible room. VERY IMPORTANT: Answer only the room name you choose and nothing else."
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
        
        coherent_ans = False
        #Process the model's response
        if model_response == 'Bathroom 2':
            grid[4, 3] = (True, grid[4, 3][1], grid[4,3][2])
            user_message = f"Oh here is my hair dryer. Well done!"
            print(f"User message: {user_message}")
            f.write(f"User message: {user_message}\n")
        else:
            for i in range(5):
                for j in range(5):
                    if (grid[i, j][1] == current_room[1]):
                        grid[i, j] = (True, grid[i, j][1], grid[i, j][2])
                        break
            for i in range(5):
                for j in range(5):
                    if grid[i, j][1] == model_response:
                        current_room = grid[i, j]
                        coherent_ans = True
                        break
        if (coherent_ans == False)or(grid[4, 3][0] == True):
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
                
        
'''
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
'''
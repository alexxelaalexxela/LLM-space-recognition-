from openai import OpenAI
import numpy as np
import sys

# Initialize the client
client = OpenAI()

#grids definition
# Define the compound data type: one bool, one float, and one string
# 'U10' means Unicode string of maximum length 10
dtype = [('bool', bool), ('float', float), ('string', 'U300')]


def describe_image(image_path):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You will be asked to navigate through a visual representation of rooms connected by doors."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": image_path
                    }
                ]
            },
            {
                "role": "user",
                "content": "Can you describe what you see?"
            }
        ]
    )
    return response.choices[0].message.content

image_path = 'https://www.dropbox.com/scl/fi/a6527edtnuzica6ymnge0/maze1.PNG?rlkey=d8kimr2wsz93uyzv4nqel9w26&dl=0'

# Initialize the conversation history
conversation_history = [
    {"role": "system", "content": "You will be navigating through rooms that you see on the picture. Each room is connected to one or several rooms, as you can observe. I will give you starting and goal room, and your are going to describe step by step the different rooms that you are going to go to."},
]


maze_description = describe_image(image_path)
print(maze_description)

current_room = 2  # Starting point
goal_room = 15     # Destination

while current_room != goal_room:
    # Construct the prompt to ask the model for the next room number based on the image
    prompt_message = "Based on the image of the maze I provided earlier, from room number {}, where should I go next to reach room number 15? VERY IMPORTANT: Answer only the room number you choose and nothing else."

    # Ask the model for the next step based on the current room
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history + [{"role": "user", "content": prompt_message.format(current_room)}]
    )

    # Extract the model's response and update the conversation history
    model_response = completion.choices[0].message.content.strip()
    conversation_history.append({"role": "system", "content": model_response})

    # Print model's choice (for the user to see in this script simulation)
    print(f"Model's choice: {model_response}")

    # Validate and update current room based on model's response
    if model_response.isdigit():
        chosen_room = int(model_response)
        # Include additional validation if necessary
        current_room = chosen_room
    else:
        print("Received an invalid response from the model. Expected a room number. Exiting.")
        break

    # Check if the goal has been reached
    if current_room == goal_room:
        print("You have reached room 8, the goal. Well done!")
        break


'''
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

'''





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
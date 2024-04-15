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
# Here, the 'grid' will have a shape of 3x3, and each cell will be able to hold our compound data
beginner_grid = np.zeros((3, 3), dtype=dtype)

# Assigning values
beginner_grid[0, 0] = (False, 1, 'This square is not accessible, choose another number and answer only this number.')
beginner_grid[0, 1] = (True, 2, 'You are on square 2. To your left, square 3 is occupied; to your right, square 1 is occupied; in front of you, square 5 is free; behind you, there is no square. Where will you go ? VERY IMPORTANT: Answer only the number you choose and nothing else.')
beginner_grid[0, 2] = (False, 3, 'This square is not accessible, choose another number and answer only this number.')

beginner_grid[1, 0] = (False, 4, 'You are on square 4. To your left, square 5 is free; to your right, there is no square; in front of you, square 7 is free; behind you, square 1 is occupied. Where will you go? VERY IMPORTANT: Answer only the number you choose and nothing else.')
beginner_grid[1, 1] = (False, 5, 'You are on square 5. To your left, square 6 is free; to your right, square 4 is free; in front of you, square 8 is occupied; behind you, square 2 is free. Where will you go? VERY IMPORTANT: Answer only the number you choose and nothing else.')
beginner_grid[1, 2] = (False, 6, 'You are on square 6. To your left, there is no square; to your right, square 5 is free; in front of you, square 9 is free; behind you, square 3 is occupied. Where will you go? VERY IMPORTANT: Answer only the number you choose and nothing else.')

beginner_grid[2, 0] = (False, 7, 'Well done, you have reached the exit!')
beginner_grid[2, 1] = (False, 8, 'This square is not accessible, choose another number and answer only this number.')
beginner_grid[2, 2] = (False, 9, 'You are on square 9. To your left, there is no square; to your right, square 8 is occupied; in front of you, there is no square; behind you, square 6 is free. Where will you go? VERY IMPORTANT: Answer only the number you choose and nothing else.')


# Initialize the conversation history
conversation_history = [
    {"role": "system", "content": "You are in a grid with some free squares where you can move and some occupied squares where movement is not possible. Starting from the starting square number and your goal is to reach a designated square somewhere in the grid. At each step, I will describe your options. VERY IMPORTANT: Answer only the number you choose and nothing else."},
]

#Initialize position
current_square = beginner_grid[0,1]
previous_square = current_square


while beginner_grid[2,2][0] == False:

    if(current_square[1]==7):
        exit()
    if (current_square[0] == False) or (current_square[1] == 2):
        user_message = current_square[2]
    else:
        user_message = f"You are on square  {current_square[1]}. You already know what are your possible options since you already been there. Where will you go ? Choose an accessible square. VERY IMPORTANT: Answer only the number you choose and nothing else."
    conversation_history.append({"role": "user", "content": user_message})
    print(f"User message: {user_message}")
    # Make the API request with the updated conversation history
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history
    )

    # Extract the model's response and update the conversation history
    model_response = completion.choices[0].message.content.strip()
    conversation_history.append({"role": "system", "content": model_response})

    print(f"Model's choice: {model_response}")
        
    #Process the model's response
    if model_response.isdigit() and 1 <= int(model_response) <= 9:
        # Find the corresponding square in beginner_grid


        for i in range(3):
            for j in range(3):
                if beginner_grid[i, j][1] == current_square[1]:
                    beginner_grid[i, j] = (True, beginner_grid[i, j][1], beginner_grid[i, j][2])
                if beginner_grid[i, j][1] == int(model_response):
                    current_square = beginner_grid[i, j]
                    break
            else:
                continue
            break
    else:
        # Escape the code
        manual_user_message = input("INTERVENTION EXT: ")
        user_message = manual_user_message
        conversation_history.append({"role": "user", "content": user_message})

from openai import OpenAI
import numpy as np
import sys

# Initialize the client
client = OpenAI()

# grids definition
# Define the compound data type: one bool, one float, and one string
# 'U10' means Unicode string of maximum length 10
dtype = [('bool', bool), ('name', 'U20'), ('string', 'U400')]

# Initialize an array with the defined data type, filled with default values
grid = np.zeros((5,18), dtype=dtype)

# Assigning values
grid[0, 0] = (False, 'lift D', 'You are in the "lift D". In front of you there is "corridor D". You can reach every floor of the building: floor D by saying "lift D", floor E by saying "lift E", floor F by saying "lift F", floor G by saying "lift G", floor H by saying "lift H". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[0, 1] = (False, 'stairs D', 'You are in the "stairs D". In front of you there is "corridor D". You can go up to floor E by saying "stairs E". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[0, 2] = (False, 'corridor D', 'You are in the "corridor D". To your right there is "lift D", to your left there are "stairs D". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')


grid[1, 0] = (True, 'entrance hall', 'You are in the "entrance hall". In front of you there is a "desk area E" and "corridor E", to your right there is an "open space", behind you there is the "street". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[1, 1] = (False, 'street', 'You are in the "street". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[1, 2] = (False, 'desk area E', 'You are in the "desk area E". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[1, 3] = (False, 'corridor E', 'You are in the "corridor E". In front of you there is "corridor E2", to your right there is "lift E", to your left there are "stairs E". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[1, 4] = (False, 'open space E', 'You are in the "open space E". To your right "room E308", in front of you there are "big stairs". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[1, 5] = (False, 'room E308', 'You are in the "room E308". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[1, 6] = (False, 'big stairs', 'You are in the "big stairs". From these you can go up to "hallway F", or go down to "open space E". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[1, 7] = (False, 'stairs E', 'You are in the "stairs E". In front of you there is "corridor E".You can go up to floor F by saying "stairs F", or go down to floor D by saying "stairs D". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[1, 8] = (False, 'lift E', 'You are in the "lift E". In front of you there is "corridor E".You can reach every floor of the building: floor D by saying "lift D", floor E by saying "lift E", floor F by saying "lift F", floor G by saying "lift G", floor H by saying "lift H". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[1, 9] = (False, 'corridor E2', 'You are in the "corridor E2". In front of you there is "room E226" and the "Street". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[1, 10] = (False, 'room E226', 'You are in the "room E226". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')

grid[2, 0] = (False, 'hallway F', 'You are in the "hallway F". Beehind you there is "corridor F", in front of you there is the "canteen". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[2, 1] = (False, 'corridor F', 'You are in the "corridor F". To your right there are "stairs F", to your right there is the "lift F", in front of you there is the "hallway F". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[2, 2] = (False, 'lift F', 'You are in the "lift F". In front of you there is "corridor F".You can reach every floor of the building: floor D by saying "lift D", floor E by saying "lift E", floor F by saying "lift F", floor G by saying "lift G", floor H by saying "lift H". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[2, 3] = (False, 'stairs F', 'You are in the "stairs F". In front of you there is "corridor F".You can go down to floor E by saying "stairs E", or you can go up to floor G by saying "stairs G". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[2, 4] = (False, 'canteen', 'You are in the "canteen". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')

grid[3, 0] = (False, 'corridor G', 'You are in the "corridor G". To your right there is "lift G" and the "bathroom G", to your left there are "stairs G". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 1] = (False, 'lift G', 'You are in the "lift G". In front of you there is "corridor G".You can reach every floor of the building: floor D by saying "lift D", floor E by saying "lift E", floor F by saying "lift F", floor G by saying "lift G", floor H by saying "lift H". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 2] = (False, 'stairs G', 'You are in the "stairs G". In front of you there is "corridor G".You can go down to floor F by saying "stairs F", or you can go up to floor H by saying "stairs H". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 3] = (False, 'bathroom G', 'You are in the "toilet G". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 4] = (False, 'corridor G N1', 'You are in the "corridor G N1". To your right there is the "open space G", to your left there is "corridor G N2", in front of you there is "room G223" and "room G222". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 5] = (False, 'open space G', 'You are in the "open space G". To your right there is "corridor G N1" and "corridor G S1", behind you there is "room G203". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 6] = (False, 'corridor G N2', 'You are in the "corridor G N2". Behind you there is "corridor G S2", in front of you there is "room G219". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 7] = (False, 'room G223', 'You are in the "room G223". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 8] = (False, 'room G222', 'You are in the "room G222". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 9] = (False, 'room G203', 'You are in the "room G203". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 10] = (False, 'corridor G S2', 'You are in the "corridor G S2". In front of you there is "corridor G N2", behind you there is "room G207" and "room G210", to your left there is "corridor G S1". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 11] = (False, 'room G219', 'You are in the "room G219". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 12] = (False, 'room G207', 'You are in the "room G207". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 13] = (False, 'room G210', 'You are in the "room G210". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 14] = (False, 'corridor G S1', 'You are in the "corridor G S1". To your left there is "open space G", to your right there is "corridor G S2", behind you there is "room G204" and "room G205". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 15] = (False, 'room G204', 'You are in the "room G204". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[3, 16] = (False, 'room G205', 'You are in the "room G205". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')


grid[4, 0] = (False, 'corridor H', 'You are in the "corridor H". In front of you there is "corridor H".To your right there is "lift H" and the "bathroom H", to your left there are "stairs H", in front of you there is "corridor H N1", behind you there is "corridor H S1". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 1] = (False, 'lift H', 'You are in the "lift H". In front of you there is "corridor H".You can reach every floor of the building: floor D by saying "lift D", floor E by saying "lift E", floor F by saying "lift F", floor G by saying "lift G", floor H by saying "lift H". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 2] = (False, 'stairs H', 'You are in the "stairs H". You can go down to floor G by saying "stairs G". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 3] = (False, 'bathroom H', 'You are in the "bathroom 2". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 4] = (False, 'corridor H N1', 'You are in the "corridor H N1". To your right there is the "open space H", to your left there is "corridor H N2", in front of you there is "room H223" and "room H222". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 5] = (False, 'open space H', 'You are in the "open space H". To your right there is "corridor H N1" and "corridor H S1", to your left there is the "rooftop", behind you there is "room H203". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 6] = (False, 'corridor H N2', 'You are in the "corridor H N2". Behind you there is "corridor H S2", in front of you there is "room H219". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 7] = (False, 'room H223', 'You are in the "room H223". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 8] = (False, 'room H222', 'You are in the "room H222". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 9] = (False, 'rooftop', 'You are in the "rooftop". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 10] = (False, 'room H203', 'You find it ! Well done !')
grid[4, 11] = (False, 'corridor H S2', 'You are in the "corridor H S2". In front of you there is "corridor H N2", behind you there is "room H207" and "room H210", to your left there is "corridor H S1". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 12] = (False, 'room H219', 'You are in the "room H219". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 13] = (False, 'room H207', 'You are in the "room H207". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 14] = (False, 'room H210', 'You are in the "room H210". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 15] = (False, 'corridor H S1', 'You are in the "corridor H S1". To your left there is "open space H", to your right there is "corridor H S2", behind you there is "room H204" and "room H205". Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 16] = (False, 'room H204', 'You are in the "room H204". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')
grid[4, 17] = (False, 'room H205', 'You are in the "room H205". There is no new place to go. Where would you like to go next ? VERY IMPORTANT: Answer only the name of the place you want to go and nothing else.')

# Initialize the conversation history

conversation_history = [
{"role": "system", "content": "You are a new student at ETH Zürich, you are in the entrance hall of a building and you are trying to find professor in room H203, and I will describe the other rooms you can directly access from your current location. Use exactly the correct name of the room as they are proposed to you, no modification on the majusclues and the small letters."},
]

#Initialize position
current_room = grid[1,0]
nonsense = False

with open('test_LEE_4_turbo.txt', 'a') as f:

    while grid[4,10][0] == False:
        if not nonsense:
            if (current_room[0] == False) or (current_room[1] == 'entrance hall'):
                user_message = current_room[2]
            else:
                user_message = f"You are in the  {current_room[1]}. You already know what are your possible options since you already been there. Where will you go ? Choose an accessible room. VERY IMPORTANT: Answer only the name of the place you want to go and nothing else."
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
        
        coherent_ans = False
        #Process the model's response
        if model_response == 'room H203':
            grid[4, 3] = (True, grid[4, 3][1], grid[4,3][2])
            user_message = f"Oh here is the room. Well done!"
            print(f"User message: {user_message}")
            f.write(f"User message: {user_message}\n")
        else:
            found = False
            for i in range(5):
                for j in range(18):
                    if (grid[i, j][1] == current_room[1]):
                        grid[i, j] = (True, grid[i, j][1], grid[i, j][2])
                        found = True
                        break
                if found:
                    break

            for i in range(5):
                for j in range(18):
                    if grid[i, j][1] == model_response:
                        current_room = grid[i, j]
                        coherent_ans = True
                        nonsense = False
                        break
                if coherent_ans:
                    break

        if not coherent_ans:
            nonsense = True
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

        if (grid[4, 10][0] == True):
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
                model="gpt-4-turbo",
                messages=conversation_history
                )

                model_response = completion.choices[0].message.content.strip()
                conversation_history.append({"role": "system", "content": model_response})
                print(f"Model's choice: {model_response}")
                f.write(f"Model's choice: {model_response}\n")  # Write to the file
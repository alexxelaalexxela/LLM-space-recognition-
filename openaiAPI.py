from openai import OpenAI
import mazeCreation


data = mazeCreation.dataGen((3, 3), 5)
print(data[0][0])
adjacent = mazeCreation.find_adjacent_letters(data[0][0][0], data[0][0][1])
start = data[0][0][1]
end = data[0][0][2]

client = OpenAI()

path = []
path.append(start)
for i in range(20):

    adjacent_letters_str = ", ".join(adjacent)
    pathstr = ", ".join(path)
    '''completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you are in a maze and you have to find the exit, all the case correspond to a different letter, take in count all the previous informations. just answer the letter of th room/way you choose"},
            {"role": "user",
                "content": f"you are in the room {start}, the room around you are the ({adjacent_letters_str}), you already look into these room ({pathstr}), answer only the letter of the room you choose to discover"},
        ]
    )'''
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you are in a maze and you have to find the exit, all the case correspond to a different letter, take in count all the previous informations to find the path. Just answer the letter of the room/way you choose"},
            {"role": "user",
                "content": f"you are in the room {start}, the room around you are the ({adjacent_letters_str}), answer only the letter of the room you choose to discover to find an exit. Tri to not take the same letter as before to find a new path "},
        ]
    )
    start = completion.choices[0].message.content
    path.append(start)
    print("current : " + start)
    if (start == end):
        print("found")
        break
    adjacent = mazeCreation.find_adjacent_letters(data[0][0][0], start)
    print(adjacent)

print(path)
# print(completion.choices[0].message.content)

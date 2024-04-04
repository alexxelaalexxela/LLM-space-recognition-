from openai import OpenAI
import mazeCreation


data = mazeCreation.dataGen((2, 2), 10)
pourc = 0
for o in range(10):

    adjacent = mazeCreation.find_adjacent_letters(
        data[0][o][0], data[0][o][1], data[0][o][1])
    start = data[0][o][1]
    end = data[0][o][2]
    client = OpenAI()
    path = []
    path.append(start)
    for i in range(20):
        print(data[0][o])
        adjacent_letters_str = " or ".join(adjacent)
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
                    "content": f"you are in the room {start}, choose among the letter (room) around you : {adjacent_letters_str}, you already look into these rooms : {pathstr}. Tri not to take the same letter as before to find a new path. VERY IMPORTANT : answer only the letter of the room you choose like this : 'letter' "},
            ]
        )
        print(f"you are in the room {start}, choose among the room around you : {adjacent_letters_str}, you already look into these rooms : {pathstr}. Tri not to take the same letter as before to find a new path. VERY IMPORTANT : answer only the letter of the room you choose like this : 'letter' ")
        start = completion.choices[0].message.content
        print("word complete : " + start)
        words = start.split()
        valid_letters = [word for word in words if len(
            word) == 1]

        if valid_letters:
            start = valid_letters[-1]
            print("valide : " + start)
        else:
            print("Aucune lettre valide trouvée.")
        if start.isupper():

            start = start.lower()
        path.append(start)
        print("current : " + start)
        if (start == end):
            print("found")
            pourc = pourc + 1
            break
        adjacent = mazeCreation.find_adjacent_letters(data[0][o][0], start)
        print(adjacent)

print(path)
print("pourcentage")
print(pourc)
# print(completion.choices[0].message.content)

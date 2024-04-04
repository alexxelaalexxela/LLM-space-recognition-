import torch
from openai import OpenAI
import mazeCreation
import torchvision
import networkx as nx
import matplotlib.pyplot as plt
import torch.nn.functional as F


data = mazeCreation.dataGen((2, 2), 10)

print(data[0][4][0])
print(data[1][4])
print("------dat---------")

pourc = 0

for o in range(10):
    print("--------")
    print(data[0][o][0])
    print("--------")
    letters = [item for sublist in data[0][o][0]
               for item in sublist if isinstance(item, str) and item.isalpha()]

    adjacent, corres = mazeCreation.find_adjacent_letters(
        data[0][o][0], data[0][o][1], data[0][o][1])

    start1 = data[0][o][1]
    past = start1
    end = data[0][o][2]
    client = OpenAI()
    path = []
    path.append(start1)
    for i in range(20):
        print(data[0][o])
        adjacent_letters_str = ", ".join(adjacent)
        adjacent_corres_str = ", ".join(corres)
        pathstr = ", ".join(path)

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "you are in a maze and you have to find the exit, all the case correspond to a different letter, take in count all the previous informations to find the path. Just answer the letter of the room/way you choose"},
                {"role": "user",
                    "content": f"you are in the room : {start1}, you can go : {adjacent_corres_str} corresponding to the letter respectively : {adjacent_letters_str}. VERY IMPORTANT : answer only the letter of the room you choose like this : 'letter' "},
            ]
        )
        print(f"you are in the room {start1}, you choose to {adjacent_corres_str} corresponding to the letter respectively : {adjacent_letters_str}. You already went to these room : {pathstr}. VERY IMPORTANT : answer only the letter of the room you choose like this : 'choosen letter' ")

        start = completion.choices[0].message.content
        incre = 0
        while ((len(start) > 1 or start not in letters) and incre < 5):  # rajouter start.minuscule
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "you are in a maze and you have to find the exit, all the case correspond to a different letter, take in count all the previous informations to find the path. Just answer the letter of the room/way you choose"},
                    {"role": "user",
                     "content": f"you are in the room : {start1}, you can go : {adjacent_corres_str} corresponding to the letter respectively : {adjacent_letters_str}. You already went to these room : {pathstr}. VERY IMPORTANT : answer only the letter of the room you choose like this : 'letter' "},
                    {"role": "system", "content": f"{start}"},
                    {"role": "user",
                     "content": f"you have to choose among the letter given and like this 'letter'"},
                ]
            )
            start = completion.choices[0].message.content
            if len(start) == 3:

                split = start.split()
                if len(split) > 1:
                    start = split[1]
            print(start)
            incre = incre + 1

        if (incre == 4):
            break

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
        print(
            f"start est actuelllement : {start}, et le resulta est : {len(start)} ")
        if start.isalpha() and (len(start) == 1):
            path.append(start)
        else:
            start = past
        print("current : " + start)
        if (start == end):
            print("found")
            pourc = pourc + 1
            break
        print(f"new start {start}")
        adjacent, corres = mazeCreation.find_adjacent_letters(
            data[0][o][0], start, past)
        past = start
        print(adjacent + corres)

    if start == end:
        new_matrix = [[2 if item in path else (1 if isinstance(
            item, str) and item.isalpha() else 0) for item in row] for row in data[0][o][0]]

        images = F.one_hot(torch.tensor(new_matrix, dtype=torch.int64))

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
        nx.draw(data[2][o], pos={node: (node[1], 4-node[0])
                for node in data[2][o].nodes}, node_color=data[2][o].colors, ax=ax1)
        ax2.imshow(torchvision.transforms.ToPILImage()(
            data[1][o][0].permute(2, 0, 1).float()), interpolation="none")
        ax3.imshow(torchvision.transforms.ToPILImage()(
            images.permute(2, 0, 1).float()), interpolation="none")
        fig.suptitle(
            f'The number of iteration was : {len(path)}, and the path was : {path}', fontsize=12)
        plt.show()
    else:
        print("NOT WORKING BITCH")

    print(path)


print("pourcentage")
print(pourc)
# print(completion.choices[0].message.content)

import string
import torch
import torchvision
import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import torch.nn.functional as F


def create_dataset(size, num_mazes):
    imagedata = []
    images = []
    graphs = []
    x = []
    y = []
    for _ in range(num_mazes):
        G = nx.grid_2d_graph(size[0], size[1])
        for e in G.edges():
            G[e[0]][e[1]]['weight'] = random.uniform(0, 1)
        T = nx.minimum_spanning_tree(G)
        start, end = random.sample(list(T.nodes), k=2)
        path = nx.shortest_path(T, source=start, target=end)

        # Add graph
        # nx.set_node_attributes(T, ['blue' if n in [start, end] else 'green' for n in T.nodes], 'color')
        T.colors = ['blue' if n in [start, end] else 'green' for n in T.nodes]
        graphs.append(T)

        # Create images
        image = np.zeros((size[0]*2+1, size[1]*2+1))
        image_solution = np.zeros((size[0]*2+1, size[1]*2+1))
        for e in T.edges():
            image[e[0][0] + e[1][0] + 1][e[0][1] + e[1][1] + 1] = 1
            image_solution[e[0][0] + e[1][0] + 1][e[0][1] + e[1][1] +
                                                  1] = 1 if not (e[0] in path and e[1] in path) else 2

        for n in T.nodes():
            image[n[0]*2+1][n[1]*2+1] = 2 if n in [start, end] else 1
            image_solution[n[0]*2+1][n[1]*2+1] = 2 if n in [start,
                                                            end] else (1 if not n in path else 2)
        imagedata.append(image)

        images.append((F.one_hot(torch.tensor(image, dtype=torch.int64)), F.one_hot(
            torch.tensor(image_solution, dtype=torch.int64))))
        # x.append(F.one_hot(torch.tensor(image, dtype=torch.int64)))
        # y.append(F.one_hot(torch.tensor(image_solution, dtype=torch.int64)))
    return imagedata, images, graphs


# @title


def show_graph_and_images(graph, images):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
    nx.draw(graphs[0], pos={node: (node[1], 4-node[0])
            for node in graph.nodes}, node_color=graph.colors, ax=ax1)
    ax2.imshow(torchvision.transforms.ToPILImage()(
        images[0].permute(2, 0, 1).float()), interpolation="none")
    ax3.imshow(torchvision.transforms.ToPILImage()(
        images[1].permute(2, 0, 1).float()), interpolation="none")
    plt.show()


def replace_with_unique_letters(matrix):
    # Find the total number of 1s and 2s to replace
    replaced_matrix = np.empty(matrix.shape, dtype=object)
    unique_counts = np.sum(matrix == 1) + np.sum(matrix == 2)

    # Generate enough letters (or letter combinations if necessary)
    letters = list(string.ascii_lowercase)
    if unique_counts > 26:
        # Generate combinations like 'aa', 'ab', ...
        letters += [a+b for a in letters for b in letters]

    # Shuffle letters to get them in random order
    random.shuffle(letters)

    # Iterator of letters
    letters_iter = iter(letters)
    first = 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] == 1 or matrix[i, j] == 2:
                replaced_matrix[i, j] = next(letters_iter)
                if matrix[i, j] == 2 and first == 0:
                    startn = replaced_matrix[i, j]
                    first = 1
                elif matrix[i, j] == 2 and first == 1:
                    lastn = replaced_matrix[i, j]
            else:
                replaced_matrix[i, j] = matrix[i, j]

    return replaced_matrix, startn, lastn


imagedata, images, graphs = create_dataset((3, 3), 10)


def dataGen(size, num_mazes):
    imagedata, images, graphs = create_dataset((3, 3), 10)
    imageLetterss = []
    for i in range(len(imagedata)):
        imageletter, start, last = replace_with_unique_letters(imagedata[0])
        data = [imageletter, start, last]
        imageLetterss.append(data)
    return imageLetterss, images, graphs


'''test, imagestest, graphstest = dataGen((3, 3), 5)

print("start : " + test[0][1] + ", last :  " + test[0][2])
print(test[0][0])

show_graph_and_images(graphstest[0], imagestest[0])
'''


def find_adjacent_letters(matrix, letter):
    # Find the position of the start letter
    start_pos = np.where(matrix == letter)
    if start_pos[0].size == 0:
        return "Start letter not found in the matrix."

    # Coordinates of the start letter
    start_row, start_col = start_pos[0][0], start_pos[1][0]

    # Vector to store adjacent letters
    adjacent_letters = []

    # Check each direction (up, down, left, right) for adjacent letters
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Left, Right, Up, Down
    for dr, dc in directions:
        new_row, new_col = start_row + dr, start_col + dc
        # Check if the new position is valid and not the end letter
        if 0 <= new_row < matrix.shape[0] and 0 <= new_col < matrix.shape[1]:
            adjacent_value = matrix[new_row, new_col]
            if adjacent_value not in [0] and isinstance(adjacent_value, str):
                adjacent_letters.append(adjacent_value)

    return adjacent_letters

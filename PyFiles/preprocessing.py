import os
import random

import networkx

import PyFiles.constants as constants

import cv2
import numpy
import pandas
from matplotlib import pyplot as plt

from PyFiles.line import Line


def read_images(folder: str) -> list:
    images = []

    files = os.listdir(folder)
    files.sort(key=lambda x: int(x.split('.')[0]))

    for file in files:
        try:
            image = cv2.imread(os.path.join(folder, file), cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, (constants.IMAGE_WIDTH, constants.IMAGE_HEIGHT))
            images.append(image)
        except Exception:
            print(Exception.__context__)

    return images


def read_matrix(file_path: str) -> tuple[numpy.ndarray, numpy.ndarray]:
    frame = pandas.read_csv(file_path)

    matrix = []

    for value in frame["Matrix"]:
        value = value.replace(".", ",")
        value = value[1:-1]
        value = value.replace(" ", "")
        value = value.split("\n")

        matrix.append(numpy.array([numpy.fromstring(line[1:-1], sep=",").tolist() for line in value]))

    return convert_to_15x15(matrix)


def convert_to_15x15(matrix):
    result = []
    lengths = []

    for value in matrix:
        lengths.append(len(value))

        fifteen = numpy.zeros((15, 15))
        fifteen[:len(value), :len(value)] = value

        result.append(fifteen)

    return numpy.array(result), numpy.array(lengths)


def to_canny(images):
    canny_images = []

    for image in images:
        canny_images.append(cv2.Canny(image, 80, 150))

    return numpy.array(canny_images)


def plot_random_images(source, *args, **kwargs):
    plt.imshow(random.choice(source), *args, **kwargs)


def merge_lines(lines, radius, threshold_degree):
    L = []

    for line in lines:
        x0, y0, x1, y1 = line[0]

        L.append(Line(x0, y0, x1, y1))

    # concatenated = L.copy()

    # # for line in L:
    # #   line.find_family(concatenated, radius, threshold_degree)

    # # result = concatenated.copy()

    # for line in L:
    #    line.concat_lines(concatenated, radius, threshold_degree)

    return L  # result


def make_graph(nodes):
    graph = networkx.Graph()

    for node in nodes:
        graph.add_node(node.index)

    all_nodes_edges = {node: node.edges for node in nodes}

    for node, edges in all_nodes_edges.items():
        for line in edges:
            for V, E in all_nodes_edges.items():
                if line in E and node is not V:
                    graph.add_edge(node.index, V.index)

    return graph

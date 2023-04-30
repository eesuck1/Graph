import math
import random

import cv2
import networkx
import numpy
from matplotlib import pyplot as plt

from PyFiles.graph import RandomGraph
import PyFiles.preprocessing as preprocess
import PyFiles.constants as constants
from PyFiles.node import Node


def main():
    random_graph = RandomGraph()

    # random_graph.generate_graph_data(200, "G:\Мій диск\GraphImages\ShortImages", "G:\Мій диск\GraphImages\Matrix20k", "short_matrix")

    random_graph.big_graph()

    # images = preprocess.read_images(constants.IMAGES_PATH)
    # matrix, edges = preprocess.read_matrix("/content/drive/MyDrive/GraphImages/Matrix20k/short_matrix.csv")
    #
    # I = 85  # random.randint(0, len(images))
    #
    # circle_image = images[I]
    # circle_image = cv2.medianBlur(circle_image, 5)
    # canny_image = cv2.Canny(circle_image, 100, 150)
    #
    # circles = cv2.HoughCircles(circle_image, cv2.HOUGH_GRADIENT, minRadius=5, maxRadius=50, dp=1.0, minDist=30,
    #                            param1=50, param2=30)
    #
    # V = []
    # L = None
    #
    # for (index, circle) in enumerate(circles[0]):
    #     x0, y0, radius = numpy.int16(circle)
    #
    #     node = Node(x0, y0, radius, index, images[I])
    #     # node.predict_sub_image()
    #
    #     V.append(node)
    #
    # distances = []
    #
    # for node in V:
    #     distances.append(node.find_distance_to_circles(V))
    #
    # lines = cv2.HoughLinesP(canny_image, 1, numpy.pi / 180, 50,
    #                         minLineLength=math.floor(numpy.array(distances).flatten().min() * 0.8),
    #                         maxLineGap=random.choice(V).radius * 2)
    #
    # try:
    #     L = preprocess.merge_lines(lines, circles[0][0][2], 15)
    #
    #     for line in L:
    #         x1, y1, x2, y2 = line.get_coordinates()
    #         cv2.line(images[I], (x1, y1), (x2, y2), (0, 0, 255), 3)
    #
    #     plt.imshow(cv2.cvtColor(images[I], cv2.COLOR_BGR2RGB))
    # except:
    #     print("no edges")
    #
    # for node in V:
    #     node.find_edges(L, V)
    #
    # for node in V:
    #     # if not node.edges:
    #     #   continue
    #
    #     x0, y0, radius = numpy.uint16(numpy.around(node.get_parameters()))
    #
    #     cv2.circle(images[I], (x0, y0), radius, (0, 255, 0), 2)
    #
    #     # cv2.circle(images[I],(x0, y0), 2, (0,0,255), 3)
    #
    # plt.imshow(cv2.cvtColor(images[I], cv2.COLOR_BGR2RGB))
    #
    # G = preprocess.make_graph(V)
    #
    # position = networkx.kamada_kawai_layout(G)
    # networkx.draw(G, position, with_labels=True)
    # plt.show()
    #
    # M = networkx.to_numpy_array(G).astype(int)


if __name__ == "__main__":
    main()

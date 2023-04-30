import os

import cv2
import numpy
import typing
from keras.models import load_model

import PyFiles.line
import PyFiles.constants as constants


class Node:
    def __init__(self, x0, y0, radius, index, image):
        self.x0 = x0
        self.y0 = constants.IMAGE_HEIGHT - y0
        self.radius = radius
        self.index = index

        self.edges = []
        self.sub_image = image[y0 - radius: y0 + radius, x0 - radius: x0 + radius].copy()

    def find_distance_to_circle(self, circle: typing.Any) -> float:
        return numpy.sqrt((self.x0 - circle.x0) ** 2 + (self.y0 - circle.y0) ** 2) - self.radius - circle.radius

    def find_distance_to_circles(self, circles: list[typing.Any]) -> list[float]:
        result = []

        for circle in circles:
            if self is circle:
                continue

            result.append(self.find_distance_to_circle(circle))

        return result

    def find_distance_to_line(self, line: PyFiles.line.Line) -> tuple[float, float]:
        start_distance = numpy.sqrt((self.x0 - line.x0) ** 2 + (self.y0 - line.y0) ** 2)
        end_distance = numpy.sqrt((self.x0 - line.x1) ** 2 + (self.y0 - line.y1) ** 2)

        return start_distance, end_distance

    def predict_sub_image(self) -> None:
        digits = load_model(os.path.join(constants.MODELS_PATH, constants.DIGITS_MODEL_NAME))

        image = cv2.resize(self.sub_image, (constants.DIGIT_SIZE, constants.DIGIT_SIZE)) / 255.0
        image = image.reshape(1, constants.DIGIT_SIZE, constants.DIGIT_SIZE, 1)

        self.index = numpy.argmax(digits.predict(image))

    def find_edges(self, lines: list[PyFiles.line.Line], circles: list[typing.Any]) -> None:
        min_distance = min(self.find_distance_to_circles(circles))

        for line in lines:
            if self.find_distance_to_line(line)[0] < self.radius * 2 or \
                    self.find_distance_to_line(line)[1] < self.radius * 2:
                self.edges.append(line)
            # else:
            #   print(f"Вершина {self.index} центр ({self.x0}, {self.y0}) лінія {self.find_distance_to_line(line)}")

    def get_parameters(self) -> tuple[int, int, float]:
        return self.x0, constants.IMAGE_HEIGHT - self.y0, self.radius

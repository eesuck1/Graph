import numpy
import typing

import PyFiles.constants as constants


class Line:
    def __init__(self, x0: int, y0: int, x1: int, y1: int):
        self.x0 = x0
        self.y0 = constants.IMAGE_HEIGHT - y0
        self.x1 = x1
        self.y1 = constants.IMAGE_HEIGHT - y1

        self.alpha = numpy.arctan2(self.y1 - self.y0, self.x1 - self.x0) * 180 / numpy.pi
        self.length = numpy.sqrt((self.x0 - self.x1) ** 2 + (self.y0 - self.y1) ** 2)

    def calculate_distance(self, line) -> tuple[float, float]:
        start_distance = numpy.sqrt((self.x0 - line.x0) ** 2 + (self.y0 - line.y0) ** 2)
        end_distance = numpy.sqrt((self.x1 - line.x1) ** 2 + (self.y1 - line.y1) ** 2)

        return start_distance, end_distance

    def calculate_end_distance(self, line) -> tuple[float, float]:
        self_end_distance = numpy.sqrt((self.x1 - line.x0) ** 2 + (self.y1 - line.y0) ** 2)
        line_end_distance = numpy.sqrt((self.x0 - line.x1) ** 2 + (self.y0 - line.y1) ** 2)

        return self_end_distance, line_end_distance

    def find_family(self, lines: list[typing.Any], radius: float, threshold_degree: float) -> list[typing.Any]:
        for line in lines:
            if self is line:
                break

            degree = abs(self.alpha - line.alpha)
            start_distance, end_distance = self.calculate_distance(line)

            if degree < threshold_degree and start_distance + end_distance < 8 * radius:
                lines.remove(line)

        return lines

    def concat_lines(self, lines: list[typing.Any], radius: float, threshold_degree: float):
        for line in lines:
            if self is line:
                break

            degree = abs(self.alpha - line.alpha)

            self_end_distance, line_end_distance = self.calculate_end_distance(line)

            if degree < threshold_degree and line_end_distance < radius * 2:
                lines.append(Line(self.x0, self.y0, line.x1, line.y1))
                lines.remove(self)
                lines.remove(line)

                break

            if degree < threshold_degree and self_end_distance < radius * 2:
                lines.append(Line(line.x0, line.y0, self.x1, self.y1))
                lines.remove(self)
                lines.remove(line)

                break

        return lines

    def get_info(self) -> None:
        print(f"(x0: {self.x0}, y0: {self.y0});\n(x1: {self.x1}, y1: {self.y1});\nAlpha: {self.alpha}")

    def get_coordinates(self) -> tuple[int, int, int, int]:
        return self.x0, constants.IMAGE_HEIGHT - self.y0, self.x1, constants.IMAGE_HEIGHT - self.y1

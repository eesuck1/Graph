import random
import os

import networkx
import matplotlib.pyplot as plt
import numpy
import pandas


class RandomGraph:
    def __init__(self, matrix_folder: str = "Matrix", matrix_file: str = "matrix_data.csv"):
        self.__frame__ = pandas.read_csv(os.path.join(matrix_folder, matrix_file))

        self.matrix = {
            "Matrix": []
        }

        for matrix in self.__frame__["Matrix"]:
            if matrix:
                self.matrix["Matrix"].append(numpy.array(matrix))

    @staticmethod
    def generate_random_graph(min_number_of_nodes: int, max_number_of_nodes: int,
                              min_edge_probability: float, max_edge_probability: float) -> tuple[networkx.DiGraph, numpy.array]:
        nodes = random.randint(min_number_of_nodes, max_number_of_nodes)
        edges = random.uniform(min_edge_probability, max_edge_probability)

        graph = networkx.gnp_random_graph(nodes, edges, directed=True)

        return graph, networkx.to_numpy_array(graph)

    @staticmethod
    def generate_random_color() -> str:
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def get_random_options(self) -> dict:
        options = {
            'edge_color': self.generate_random_color(),
            'node_color': random.choice([self.generate_random_color(), 'none']),
            'width': random.uniform(1, 3),
            'node_size': random.randint(300, 700),
            'with_labels': True,
        }

        return options

    @staticmethod
    def draw_graph(graph, options: dict = None) -> None:
        if options is None:
            options = {}

        position = networkx.kamada_kawai_layout(graph)

        networkx.draw(graph, position, **options)

    @staticmethod
    def create_path(folder_name: str, file_name: str) -> str:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        return os.path.join(folder_name, file_name)

    def save_graph(self, folder_name: str, file_name: str) -> None:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        plt.savefig(self.create_path(folder_name, file_name))

        figure = plt.gcf()
        figure.clf()

    def save_matrix(self, folder_name: str, file_name: str) -> None:
        frame = pandas.DataFrame(self.matrix)

        frame.to_csv(self.create_path(folder_name, file_name + ".csv"))

    def generate_graph_data(self, data_size: int, graph_folder: str, matrix_folder: str, matrix_file: str,
                            min_number_of_nodes: int = 5, max_number_of_nodes: int = 15,
                            min_edge_probability: float = 0.1, max_edge_probability: float = 0.5
                            ) -> None:
        print(f"[INFO] Start with parameters: \nData Size: {data_size}\nImages Folder: {graph_folder}\n"
              f"CSV Matrix Folder: {matrix_folder} \nNumber or nodes: {min_number_of_nodes} - {max_number_of_nodes}\n"
              f"Edge Probability: {min_edge_probability} - {max_edge_probability}")

        for graph_index in range(len(os.listdir(os.path.join(graph_folder))), data_size):
            G, matrix = self.generate_random_graph(min_number_of_nodes, max_number_of_nodes,
                                                   min_edge_probability, max_edge_probability)

            self.matrix["Matrix"].append(matrix)

            self.draw_graph(G, self.get_random_options())
            self.save_graph(graph_folder, f"{graph_index}")

        self.save_matrix(matrix_folder, matrix_file)

        print(f"[INFO] Generation Completed Successfully")

from graph import RandomGraph


def main():
    rg = RandomGraph()

    rg.generate_graph_data(5000, "Images", "Matrix", "matrix_data")


if __name__ == "__main__":
    main()

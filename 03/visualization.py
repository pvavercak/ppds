from matplotlib import pyplot as plt
import pickle


def load_from_pickle(pickle_file):
    results = dict()
    with open(pickle_file, "rb") as file_handle:
        results = pickle.load(file_handle)
    return results


def plot_results(results: dict):
    keys = [key for key in results.keys()]
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.set_xlabel(keys[0])
    ax.set_ylabel(keys[1])
    ax.set_zlabel(keys[2])
    ax.plot_trisurf(results[keys[0]], results[keys[1]],
                    results[keys[2]], cmap="viridis", edgecolor="none")
    plt.show()

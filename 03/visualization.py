import pickle


def load_from_pickle(pickle_file):
    results = dict()
    with open(pickle_file, "rb") as file_handle:
        results = pickle.load(file_handle)
    return results


def plot_results(results: dict):
    pass

import pickle

def pretty_print_dict(dict):
    for key, value in dict.items():
        print(key + ":", value, "\n")

with open('./metadata/metadata-101.pkl', 'rb') as f:
    metadata = pickle.load(f)

pretty_print_dict(metadata['J.J. Abrams'])
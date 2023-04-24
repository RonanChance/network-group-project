import pickle

def pretty_print_dict(dict):
    for key, value in dict.items():
        print(key + ":", value, "\n")

if __name__ == "__main__":
    with open('../2-network-generation/metadata/metadata-101.pkl', 'rb') as f:
        metadata = pickle.load(f)

    person = "Andrew Pouch"
    print("Metadata for:", person, "\n")
    #pretty_print_dict(metadata[person])
    pretty_print_dict(metadata[person])

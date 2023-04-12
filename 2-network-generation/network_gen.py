from filepaths_list import find_file_paths
import networkx as nx
import collections
import fileinput
import json

# recursive function that iterates the json object and extracts the names
# will be adjusting later to get generalized categories (currently getting specific credits)
def extract_names(json_obj, names_set, credits_dict):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == 'name':
                # keep track of the names
                names_set.add(value)

                # also access their respective credits
                for k, v in json_obj.items():
                    if k == 'credit':
                        credits_dict[value].add(v)
            else:
                extract_names(value, names_set, credits_dict)
    elif isinstance(json_obj, list):
        for item in json_obj:
            extract_names(item, names_set, credits_dict)

# iterates through a jsonl file and returns a dictionary of names and their count
# repetitions of a name in the same line of a json are ignored (same person in different roles in the same film is a count of 1)
def process_jsonl(path):
    i = 0
    # this is a type of dictionary that has a default value of 1
    names_dict = collections.defaultdict(int)
    credits_dict = collections.defaultdict(set)
    
    for line in fileinput.input(path):
        # load the data in json object
        data = json.loads(line)
        names_set = set()
        # add all the new names to our running set
        extract_names(data, names_set, credits_dict)
        for item in names_set:
            names_dict[item] += 1
    
    # return the sorted dictionary for this director
    return sorted(names_dict.items(), key=lambda x:x[1]), credits_dict

# function that converts the crew names (and their count), director name, and credit dictionaries to a graph
# the count of the names is the weights of the edges, and credit is put in the attribute dictionary
def list_to_graph(G, names_list, director_name, credits_dict):
    for name, weight in names_list:
        G.add_edge(director_name, name, weight=weight)

    for node in G.nodes():
        G.add_node(node, attr_dict={"credit": list(credits_dict[node])})

    return G

if __name__ == "__main__":
    '''
    This script will generate a network of directors and their crew members.
    It will be a directed and weighted network, saved as a gephi file.
    '''

    # establish a directed graph
    G = nx.DiGraph()

    # sort for our sake
    film_directors_paths = sorted(find_file_paths())
    
    for path in film_directors_paths[:1]:
        processed_data, credits_dict = process_jsonl(path)
        director_name = path.split("/")[-1].replace("-", " ").replace(".jsonl", "")
        list_to_graph(G, processed_data, director_name, credits_dict)
    
    for source, target, data in G.edges(data=True):
        print(f"{source} -> {target}, weight: {data['weight']}")

    print("Writing to gephi file...")
    nx.write_gexf(G, "network.gexf")
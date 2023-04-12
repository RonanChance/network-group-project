from filepaths_list import find_file_paths
import networkx as nx
import collections
import fileinput
import json

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

def list_to_graph(G, names_list, director_name, credits_dict):
    for name, weight in names_list:
        G.add_edge(director_name, name, weight=weight)

    for node in G.nodes():
        G.add_node(node, attr_dict={"credit": list(credits_dict[node])})

    return G

if __name__ == "__main__":
    # establish a directed graph
    G = nx.DiGraph()

    # sort for our sake
    film_directors_paths = sorted(find_file_paths())
    
    for path in film_directors_paths[:1]:
        processed_data, credits_dict = process_jsonl(path)
        director_name = path.split("/")[-1].replace("-", " ").replace(".jsonl", "")
        list_to_graph(G, processed_data, director_name, credits_dict)
        print(processed_data)
    
    for node in G.nodes():
        print(node, "hi")
    
    for source, target, data in G.edges(data=True):
        print(f"{source} -> {target}, weight: {data['weight']}")

    print("Writing to gephi file...")
    nx.write_gexf(G, "network.gexf")
from filepaths_list import find_file_paths
import networkx as nx
import collections
import fileinput
import json

def extract_names(json_obj, names_set):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == 'name':
                names_set.add(value)
            else:
                extract_names(value, names_set)
    elif isinstance(json_obj, list):
        for item in json_obj:
            extract_names(item, names_set)

def process_jsonl(path):
    i = 0
    # this is a type of dictionary that has a default value of 1
    names_dict = collections.defaultdict(int)
    
    for line in fileinput.input(path):
        # load the data in json object
        data = json.loads(line)
        # add all the new names to our running set
        names_set = set()
        extract_names(data, names_set)
        for item in names_set:
            names_dict[item] += 1
    
    # return the sorted dictionary for this director
    return sorted(names_dict.items(), key=lambda x:x[1])

# for use with get_label_data
def find_credit(name, data):
    found_list = []
    if isinstance(data, list):
        for item in data:
            found_list.extend(find_credit(name, item))
    elif isinstance(data, dict):
        if 'name' in data and data['name'] == name and 'credit' in data:
            found_list.append(data['credit'])
        for key, value in data.items():
            found_list.extend(find_credit(name, value))
    return found_list


def get_label_data(name, path):
    # print(name)
    credits = collections.defaultdict(int)
    for line in fileinput.input(path):
        data = json.loads(line)
        for credit in find_credit(name, data):
            credits[credit] += 1
    return credits


def list_to_graph(G, names_list, director_name):
    for name, weight in names_list:
        G.add_edge(director_name, name, weight=weight)
    return G

if __name__ == "__main__":
    # establish a directed graph
    G = nx.DiGraph()

    # sort for our sake
    film_directors_paths = sorted(find_file_paths())
    
    for path in film_directors_paths[:1]:
        processed_data = process_jsonl(path)
        director_name = path.split("/")[-1].replace("-", " ").replace(".jsonl", "")
        list_to_graph(G, processed_data, director_name)
    
    attr_dict = {}
    for source, target, data in G.edges(data=True):
        # target is their name
        # person_info = get_label_data(target, path).keys()
        nx.set_node_attributes(G, {target:[key for key in get_label_data(target, path).keys()]}, 'credit')

    
    for source, target, data in G.edges(data=True):
        print(f"{source} -> {target}, weight: {data['weight']}")

    print("Writing to gephi file...")
    nx.write_gexf(G, "network.gexf")
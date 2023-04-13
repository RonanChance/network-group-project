from filepaths_list import find_file_paths, find_role_names
import networkx as nx
import collections
import fileinput
import json

# Get names and information about every individual in json file
def extract_info(data):
    credits_dict = collections.defaultdict(set)
    names_set = set()

    i = 0
    for i in range(len(data["full_credits"])):
        gen_title = data["full_credits"][i]['role']
        
        for j in range(len(data["full_credits"][i]['crew'])):
            person = data["full_credits"][i]['crew'][j]['name']
            credits_dict[person].add(gen_title)
            names_set.add(person)
        
        i += 1
    return credits_dict, names_set

# iterates through a jsonl file and returns a dictionary of names and their count
# repetitions of a name in the same line of a json are ignored (same person in different roles in the same film is a count of 1)
def process_jsonl(path):
    # this is a type of dictionary that has a default value of 1
    name_weights = collections.defaultdict(int)
    credits_dict = collections.defaultdict(set)
    
    for line in fileinput.input(path):
        # load the data in json object
        data = json.loads(line)
        single_credits_dict, single_names_set = extract_info(data)
        
        # increment weights, combine credits
        for name in single_names_set:
            name_weights[name] += 1
        
        for key, value in single_credits_dict.items():
            if key in credits_dict:
                credits_dict[key] = credits_dict[key].union(value)
            else:
                credits_dict[key] = value
        
    # return the sorted dictionary for this director
    return name_weights, credits_dict

# function that converts the crew names (and their count), director name, and credit dictionaries to a graph
# the count of the names is the weights of the edges, and credit is put in the attribute dictionary
def list_to_graph(G, names_list, director_name, credits_dict):
    for name, weight in names_list.items():
        G.add_edge(director_name, name, weight=weight)

    # for name, cred in credits_dict.items():
    #     credits_dict[name] = list(cred)

    # establish 0 on every role type for each node
    role_names = find_role_names()
    for cat in role_names:
        if len(G.nodes[name]) < len(role_names):
            for name in names_list:
                G.nodes[name][cat] = 0
        # also assign zeroes for director if they haven't been assigned roles yet
        if len(G.nodes[director_name]) < len(role_names):
            G.nodes[director_name][cat] = 0
    
    for key, cred_list in credits_dict.items():
        for credit in cred_list:
            G.nodes[key][credit] = 1

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
    
    credits_dict = {}
    for path in film_directors_paths[:1]:
        name_weights, credits_dict_director = process_jsonl(path)
        director_name = path.split("/")[-1].replace("-", " ").replace(".jsonl", "")

        list_to_graph(G, name_weights, director_name, credits_dict_director)
    
    for source, target, data in G.edges(data=True):
        print(source, target, data["weight"])

    print("Writing to gephi file...")
    nx.write_gexf(G, "network.gexf")
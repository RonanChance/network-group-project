from filepaths_list import find_file_paths
import networkx as nx
import collections
import itertools
import fileinput
import argparse
import pickle
import json

# Get names and information for every individual in json file
# Returns a dictionary mapping of name and a set of roles the individual has worked
# Also returns a set of all names seen in the json object
def extract_info(data):
    credits_dict = collections.defaultdict(set)
    names_set = set()

    for i in range(len(data["full_credits"])):
        gen_title = data["full_credits"][i]['role']
        
        for j in range(len(data["full_credits"][i]['crew'])):
            person = data["full_credits"][i]['crew'][j]['name']
            credits_dict[person].add(gen_title)
            names_set.add(person)
        
    return credits_dict, names_set

# Given a json file and a graph, add nodes and edges to the graph (avoiding self-loops)
# Returns the updated graph
def process_jsonl(path, G):
    for line in fileinput.input(path):
        # load the data in json object
        data = json.loads(line)
        single_credits_dict, single_names_set = extract_info(data)
        
        # get each director name
        director_list = [director['name'] for director in data["full_credits"][0]['crew']]
        # print(director_list)

        for name in director_list:
            G.add_node(name, director=True)
            for crew in single_names_set:
                # avoid duplicate increments
                if crew in director_list:
                    continue
                elif G.has_edge(name, crew):
                    G[name][crew]['weight'] += 1
                else:
                    G.add_edge(name, crew, weight=1)

        # connect directors
        director_combinations = list(itertools.combinations(director_list, 2))
        for combo in director_combinations:
            if G.has_edge(combo[0], combo[1]):
                G[combo[0]][combo[1]]['weight'] += 1
            else:
                G.add_edge(combo[0], combo[1], weight=1)

    return G

def extract_metadata(G, paths):
    metadata = {}

    for path in paths:
        for line in fileinput.input(path):
            data = json.loads(line)
            movie_title = data["title"]
            single_credits_dict, single_names_set = extract_info(data)
            director_list = [director['name'] for director in data["full_credits"][0]['crew']]

            for name in single_names_set:
                if name in metadata:
                    metadata[name]["directors"].extend([n for n in director_list if n != name])
                    metadata[name]["movies"].add(movie_title)
                    metadata[name]["roles"].update(single_credits_dict[name])
                else:
                    metadata[name] = {"directors":[], "movies":set(), "roles":set()}

    with open('./metadata/metadata.pkl', 'wb') as f:
        pickle.dump(metadata, f)


if __name__ == "__main__":
    # set up command line parsing
    parser = argparse.ArgumentParser(description='Example script with optional argument')
    parser.add_argument('--numdirectors', type=int, help='Number of directors')
    args = parser.parse_args()

    # get the file paths
    jsonl_paths = sorted(find_file_paths())

    if args.numdirectors:
        num_directors = args.numdirectors
    else:
        num_directors = len(jsonl_paths)

    # establish an undirected graph
    G = nx.Graph()
    
    # for the first few directors, make our network
    for path in jsonl_paths[:num_directors]:
        G = process_jsonl(path, G)
        # see from console how far we are through list
        print("Finished", path)

    extract_metadata(G, jsonl_paths)
    print("Finished metadata extraction")

    gephi_filename = "./networks/network-"+str(num_directors)+".gexf"
    nx.write_gexf(G, gephi_filename)
    print("Wrote gephi file", gephi_filename)
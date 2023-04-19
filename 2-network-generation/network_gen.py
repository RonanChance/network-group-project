from filepaths_list import find_file_paths, find_role_names
import networkx as nx
import collections
import itertools
import fileinput
import argparse
import json

# Get names and information for every individual in json file
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


def process_jsonl(path, G):
    for line in fileinput.input(path):
        # load the data in json object
        data = json.loads(line)
        single_credits_dict, single_names_set = extract_info(data)
        
        # get each director name
        director_list = [director['name'] for director in data["full_credits"][0]['crew']]
        print(director_list)

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
        

        # for name in director_list:
        #     G.add_node(name, director=True)
        #     for crew in single_names_set:
        #         if name == crew:
        #             continue
        #         elif G.has_edge(name, crew):
        #             G[name][crew]['weight'] += 1
        #         else:
        #             G.add_edge(name, crew, weight=1)
    return G


if __name__ == "__main__":

    # set up command line parsing
    parser = argparse.ArgumentParser(description='Example script with optional argument')
    parser.add_argument('--numdirectors', type=int, help='Number of directors')
    args = parser.parse_args()

    # get the file paths
    film_directors_paths = sorted(find_file_paths())

    if args.numdirectors:
        num_directors = args.numdirectors
    else:
        num_directors = len(film_directors_paths)

    # establish an undirected graph
    G = nx.Graph()
    
    # for the first few directors, make our network
    for path in film_directors_paths[:num_directors]:
        G = process_jsonl(path, G)
        # see from console how far we are through list
        print("Finished", path)

    nx.write_gexf(G, "./networks/network-"+str(num_directors)+".gexf")
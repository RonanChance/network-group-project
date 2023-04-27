from .find_info import extract_info
import fileinput
import json
import pickle
import itertools
import pandas as pd

# Given a json file and a graph, add nodes and edges to the graph (avoiding self-loops)
# Returns the updated graph
def jsonl_to_network(path, G):
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
                if name not in metadata:
                    metadata[name] = {"directors":[], "movies":set(), "roles":set()}
                metadata[name]["directors"].extend([n for n in director_list if n != name])
                metadata[name]["movies"].add(movie_title)
                metadata[name]["roles"].update(single_credits_dict[name])

    for key, val in metadata.items():
        metadata[key]["num_uniq_directors"] = len(set(val["directors"]))
        metadata[key]["num_uniq_movies"] = len(val["movies"])
        metadata[key]["num_uniq_roles"] = len(val["roles"])
        # also replace sets with lists for ease of use, and sort them
        metadata[key]["movies"] = sorted(list(val["movies"]))
        metadata[key]["roles"] = sorted(list(val["roles"]))
        metadata[key]["directors"] = sorted(val["directors"])
    
    filename = './metadata/metadata-' + str(len(paths)) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(metadata, f)
    print("Wrote metadata file", filename)

    return metadata

def add_diversity_attr_to_network(G, path):
    df = pd.read_csv(path, sep=',', header=0)

    for _, row in df.iterrows():
        # get Name, Sex, Ethnicity_Race, and Labels
        name = row[1] + " " + row[0]
        sex = row[2]
        ethnicity = row[3]
        labels = row[4]
        imdb = row[5]#.split("/")[4] (not gonna split because seems convenient to have whole url)

        if G.has_node(name):     
            G.nodes[name]["sex"] = sex
            G.nodes[name]["ethnicity"] = ethnicity 
            G.nodes[name]["imdb"] = imdb

            if type(labels) == str:
                    if labels == "H":
                        G.nodes[name]['renowned'] = True
                    if labels == "Q":
                        G.nodes[name]['queer'] = True
    return G

def add_metadata_to_network(G, metadata):
    for name in metadata:
        if G.has_node(name):
            G.nodes[name]['num_uniq_directors'] = metadata[name]['num_uniq_directors']
            G.nodes[name]['num_uniq_movies'] = metadata[name]['num_uniq_movies']
            G.nodes[name]['num_uniq_roles'] = metadata[name]['num_uniq_roles']
    return G

def normalize_weights(G):
    # for each node in the network, if it is a director, normalize the weights between it and crew
    for node in G.nodes:
        if 'director' in G.nodes[node]:
            # get the number of crew connections they have (= connections - director connections)
            # also make sure it is at least 1
            # also keep track of score so we can average it
            num_crew = sum(1 for neighbor in G.neighbors(node) if not G.nodes[neighbor].get('director'))
            if num_crew == 0:
                G.nodes[node]["homogeneity_param"] = 0
                continue
            
            sum_total = 0
            for neighbor in G.neighbors(node):
                # dont update relationships between directors
                if 'director' not in G.nodes[neighbor]:
                    # norm_weight = G[node][neighbor]['weight'] / num_crew
                    norm_weight = G[node][neighbor]['weight'] / G.nodes[node]["num_uniq_movies"]
                    G[node][neighbor]['norm_weight'] = norm_weight
                    sum_total += norm_weight
            G.nodes[node]["homogeneity_param"] = (sum_total / num_crew) * G.nodes[node]["num_uniq_movies"]   
                    
    return G


# Tyler Perry
# Peter Jackson
# Clint Eastwood
# David Yates
# Christopher Nolan
# Steven Soderberg
# Steven Spielberg
# Woody Allen
# Barry Jenkins
# Wes Anderson
# Lilly Wachowski
# J.J. Abrams
# Michael Bay
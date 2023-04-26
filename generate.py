from functions.generation.find_info import find_file_paths, extract_info, extract_metadata
import networkx as nx
import pandas as pd
import itertools
import fileinput
import argparse
import json
import gzip
import os

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

def add_metadata_to_network(G, metadata):
    for name in metadata:
        if G.has_node(name):
            G.nodes[name]['num_uniq_directors'] = metadata[name]['num_uniq_directors']
            G.nodes[name]['num_uniq_movies'] = metadata[name]['num_uniq_movies']
            G.nodes[name]['num_uniq_roles'] = metadata[name]['num_uniq_roles']
    return G


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
                    norm_weight = G[node][neighbor]['weight'] / num_crew
                    G[node][neighbor]['norm_weight'] = norm_weight
                    sum_total += norm_weight
            G.nodes[node]["homogeneity_param"] = sum_total / num_crew           
                    
    return G


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
        G = jsonl_to_network(path, G)
        # see from console how far we are through list
        print("Finished", path)

    metadata = extract_metadata(G, jsonl_paths[:num_directors])
    print("Finished metadata extraction..")

    G = add_metadata_to_network(G, metadata)
    print("Added metadata to network..")

    G = add_diversity_attr_to_network(G, "directors.csv")
    print("Added diversity attributes to network..")

    G = normalize_weights(G)

    gephi_filename = "./networks/network-"+str(num_directors)+".gexf"
    gephi_filename_gz = "./networks/network-" + str(num_directors) + ".gexf.gz"

    nx.write_gexf(G, gephi_filename)
    print("Wrote gephi file:", gephi_filename)

    with open(gephi_filename, 'rb') as f_in:
        with gzip.open(gephi_filename_gz, 'wb') as f_out:
            f_out.writelines(f_in)
    print("Wrote compressed gephi file:", gephi_filename_gz)

    os.remove(gephi_filename)
    print("Deleted uncompressed file:", gephi_filename)


    sorted_homogeneity = sorted([(node, G.nodes[node]['homogeneity_param']) for node in G.nodes if 'director' in G.nodes[node]], key=lambda x: x[1], reverse=True)
    print(sorted_homogeneity)


    #
    # PLAYING AROUND HERE
    #
    # director_re_use = []
    # for node in G.nodes:
    #     if 'director' in G.nodes[node]:
    #         neighbors = list(G.neighbors(node))
    #         if len(neighbors) > 0:
    #             total_weight = sum(G[node][neighbor]['weight'] for neighbor in neighbors)
    #             movie_count = G.nodes[node]['num_uniq_movies']
    #             re_use_metric = total_weight / movie_count
    #         else:
    #             re_use_metric = 0
    #         director_re_use.append((node, re_use_metric))
    #         # print(f"Director {node} re-use metric: {re_use_metric}")

    # director_re_use.sort(key=lambda x: x[1], reverse=True)
    # for item in director_re_use:
    #     print(item)

    
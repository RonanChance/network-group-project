from functions.generation.find_info import find_file_paths
from functions.generation.net_funcs import jsonl_to_network, add_metadata_to_network, add_diversity_attr_to_network, normalize_weights, extract_metadata, remove_parsed_directors, add_norm_weights_to_network, add_homogeneity_to_network
import networkx as nx
import pandas as pd
import argparse
import gzip
import os

if __name__ == "__main__":
    # set up command line parsing
    parser = argparse.ArgumentParser(description='Example script with optional argument')
    parser.add_argument('--numdirectors', type=int, help='Number of directors')
    parser.add_argument('--directorexclusions', action='store_false', help='Exclude Parsed Directors', default=True)
    parser.add_argument('--crewexclusions', nargs='+', help='List of Roles to Exclude')
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
        G = jsonl_to_network(path, G, args.crewexclusions)
        # see from console how far we are through list
        print("Finished", path)

    metadata = extract_metadata(G, jsonl_paths[:num_directors], args.crewexclusions)
    print("Finished metadata extraction..")

    G = add_metadata_to_network(G, metadata)
    print("Added metadata to network..")

    G = add_diversity_attr_to_network(G, "directors.csv")
    print("Added diversity attributes to network..")

    # remove parsed directors if chosen
    if args.directorexclusions:
        G = remove_parsed_directors(G)

    G = add_norm_weights_to_network(G)
    print("Added normalized weights to network..")

    G = add_homogeneity_to_network(G)
    print("Added homogeneity to network..")

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
    
# Command
# python generate.py --crewexclusions 'Additional Crew' 'Animation Department' 'Art Department' 'Art Direction by' 'Camera and Electrical Department' 'Cast' 'Casting By' 'Casting Department' 'Costume and Wardrobe Department' 'Editorial Department' 'Location Management' 'Music Department' 'Produced by' 'Production Department' 'Production Management' 'Script and Continuity Department' 'Second Unit Director or Assistant Director' 'Set Decoration by' 'Stunts' 'Thanks' 'Transportation Department' 'Visual Effects by'


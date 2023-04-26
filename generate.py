from functions.generation.find_info import find_file_paths
from functions.generation.net_funcs import jsonl_to_network, add_metadata_to_network, add_diversity_attr_to_network, normalize_weights, extract_metadata
import networkx as nx
import pandas as pd
import argparse
import gzip
import os

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
    
import networkx as nx
import pandas as pd
from functions.generation.find_info import get_director_list
from functions.generation.net_funcs import normalize_weights

if __name__ == "__main__":
    director_list = get_director_list("directors.csv")

    G = nx.read_gexf('./networks/network-101.gexf.gz')
    G = normalize_weights(G)
    
    sorted_homogeneity = sorted([(node, G.nodes[node]['homogeneity_param']) for node in G.nodes if ('director' in G.nodes[node]) and (node in director_list)], key=lambda x: x[1], reverse=True)
    # print(sorted_homogeneity)




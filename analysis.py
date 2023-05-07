from functions.generation.find_info import find_file_paths, get_director_list
from functions.generation.net_funcs import normalize_weights, add_norm_weights_to_network, add_homogeneity_to_network
from functions.analysis import basic_stats
import networkx as nx
import pickle

if __name__ == "__main__":
    # with open('./metadata/metadata-101.pkl', 'rb') as f:
    #     metadata = pickle.load(f)

    # person = "J.J. Abrams"
    # print("Metadata for:", person, "\n")

    # basic_stats.pretty_print_dict(metadata[person])

    # movie_names, total_num_movies = basic_stats.find_movie_names()
    # print(movie_names)
    # print(total_num_movies)

    # Read our current network G
    G = nx.read_gexf('./networks/network-101.gexf.gz')

    # # Print role homogeneity values for every director
    path_to_csv = "./directors.csv"
    # role_homogeneity_all_dirs_dict = basic_stats.get_role_homogeneity_dict(G, path_to_csv)
    # basic_stats.pretty_print_get_role_homogeneity(role_homogeneity_all_dirs_dict)

    # # Print avg. role homogeneity value for every director
    # avg_role_homogeneity_dict = basic_stats.get_avg_role_homogeneity_dict(G,path_to_csv)
    # basic_stats.pretty_print_get_avg_role_homogeneity(avg_role_homogeneity_dict)

    # # Get avg. degree for only director nodes
    # basic_stats.get_average_degree_for_all_directors(G)

    # print(nx.average_clustering(G))

# TBF --
    # dirs = get_director_list(path_to_csv)
    # tri = {}
    # for dir in dirs:
    #     tri[dir] = nx.triangles(G,dir)

# print(nx.triangles(G,"David Lynch"))
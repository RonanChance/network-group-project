from functions.generation.find_info import find_file_paths, get_director_list
from functions.generation.net_funcs import normalize_weights
from functions.analysis import basic_stats
import networkx as nx
import pickle

if __name__ == "__main__":
    # with open('./metadata/metadata-101.pkl', 'rb') as f:
    #     metadata = pickle.load(f)

    # person = "J.J. Abrams"
    # print("Metadata for:", person, "\n")

    # basic_stats.pretty_print_dict(metadata[person])

    # print("Getting movie list and number of movies...")
    # movie_names, total_num_movies = basic_stats.find_movie_names()
    # print(movie_names)
    # print(total_num_movies)

    # Read our current network G
    G = nx.read_gexf('./networks/network-101.gexf.gz')
    G = normalize_weights(G)

    # Print role homogeneity values for every director
    path_to_csv = "./directors.csv"
    role_homogeneity_all_dirs_dict = basic_stats.get_role_homogeneity_dict(G, path_to_csv)
    basic_stats.pretty_print_get_role_homogeneity(role_homogeneity_all_dirs_dict)

    # Print avg. role homogeneity value for every director
    avg_role_homogeneity_dict = basic_stats.get_avg_role_homogeneity_dict(G,path_to_csv)
    basic_stats.pretty_print_get_avg_role_homogeneity(avg_role_homogeneity_dict)


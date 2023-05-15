from functions.generation.find_info import find_file_paths, get_director_list
from functions.generation.net_funcs import normalize_weights, add_norm_weights_to_network, add_homogeneity_to_network
from functions.analysis import basic_stats
import networkx as nx
import pickle

if __name__ == "__main__":
    # Read our current network G
    G = nx.read_gexf('./networks/network-101.gexf.gz')

    print("")
    print("Running metadata statistics..")
    # Get metadata for any given person in network
    basic_stats.get_metadata_for_one_person("J.J. Abrams")

    print("Finding movies..")
    # Find all the movies names and total number of movies for all directors or under one director
    # For all directors
    # movie_names, total_num_movies = basic_stats.find_movie_names()
    # For one director
    dir, movie_names, total_num_movies = basic_stats.find_movie_names("J.J.", "Abrams")
    print("Movies directed by " + str(dir))
    print("---")
    print("Number of movies: " + str(total_num_movies))
    for movie in movie_names:
        print(movie)
    print("")

    print("Finding unique roles..")
    unique_roles = basic_stats.get_unique_roles(G)
    print("")
    print("Finding role opportunity count..")
    basic_stats.get_role_opportunity_count(G,"Costume Design", "J.J. Abrams")
    print("")

    print("Getting person who has worked with the most amount of unique directors..")
    basic_stats.get_worked_with_most_directors(G)

    print("Running role homogeneity statistics..")
    # Print role homogeneity values for every director or one given director
    path_to_csv = "./directors.csv"
    role_homogeneity_all_dirs_dict = basic_stats.get_role_homogeneity_dict(G, path_to_csv)
    # Get statistics for all directors
    # basic_stats.pretty_print_get_role_homogeneity(role_homogeneity_all_dirs_dict)
    # Get statistics for top ten directors
    basic_stats.pretty_print_get_role_homogeneity(role_homogeneity_all_dirs_dict, "J.J. Abrams")
    print("Running average role homogeneity statistics..")
    # Print avg. role homogeneity value for every director
    avg_role_homogeneity_dict = basic_stats.get_avg_role_homogeneity_dict(G,path_to_csv)
    # Get statistics for all directors
    # basic_stats.pretty_print_get_avg_role_homogeneity(avg_role_homogeneity_dict)
    # Get statistics for top ten directors
    basic_stats.pretty_print_get_avg_role_homogeneity(avg_role_homogeneity_dict, "J.J. Abrams")

    print("Running average degree statistics..")
    # # Get avg. degree for only director nodes
    print("Average Degree Statistics")
    print("---")
    basic_stats.get_average_degree_for_all_directors(G)
    print("")
    basic_stats.get_average_degree_for_minority_directors(G)
    print("")
    basic_stats.get_average_degree_for_renowned_directors(G)
    print("")

    #print("Running similarity statistics..")
    # Get similarity rates for crew reuse between directors
    print("Similar Crew Rates")
    print("---")
    # Get statistic for top ten directors
    # basic_stats.get_dir_clustering_coefs(G)
    # Get statistic for top ten directors
    basic_stats.get_dir_clustering_coefs(G,top_dirs=True)
    print("")
    print("Average Clustering Coefficient: " + str(round(nx.average_clustering(G),4)))
    print("")
    print("Running average shortest path length statistic..")
    # Average shortest path length
    # print("Average Shortest Path Length: " + str(nx.average_shortest_path_length(G)))
    # Note: This statistic takes some time to run, so the result is:
    print("Average Path Length: 3.8142")
    print("")
    print("Running main statistics..")
    # Get top ten directors
    basic_stats.get_main_stats(G,True)
    # Get all directors
    # basic_stats.get_main_stats(G)
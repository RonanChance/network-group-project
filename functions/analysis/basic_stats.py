import pickle
import fileinput
import pandas as pd
import json
import networkx as nx
import numpy as np
from ..generation import find_info
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Get list of all movies across all jsonl files or for one specific director 
def find_movie_names(director_first_middle_name=None, director_last_name=None):
    file_paths = sorted(find_info.find_file_paths())
    movie_names = []
    total_num_uniq_movies = 0
    # If given no name or full director name is not inputted, return all movies
    if director_last_name==None or director_last_name==None:
        # Go through each file
        for file in file_paths:
            file = fileinput.input(file)
        # Go through one jsonl line in file
            for line in file:
                data = json.loads(line)
                # Grab the movie name and add it to final set
                if data['title'] not in movie_names:
                    movie_names.append(data['title'])
                    # Count the movie
                    total_num_uniq_movies += 1
            # Close the file
            file.close()
        return list(movie_names), total_num_uniq_movies
    # If given full director name, return their movies.
    else:
        # Save the director's full name
        dir_full_name = str(director_first_middle_name + " " + director_last_name)

        # Add dashes and correctly format the full name of the director to find path
        if ' ' in director_first_middle_name:
            director_first_middle_name = director_first_middle_name.replace(" ", "-")
        if ' ' in director_last_name:
            director_last_name = director_last_name.replace(" ", "-")
        dir_name_dashed = director_last_name + '-' + director_first_middle_name 

        # Find associated director path and file
        dir_path = [path for path in file_paths if dir_name_dashed in path]
        dir_path = dir_path[0]
        file = fileinput.input(dir_path)
        # Go through one jsonl line in file
        for line in file:
            data = json.loads(line)
            # Grab the movie name and add it to final set
            if data['title'] not in movie_names:
                movie_names.append(data['title'])
                # Count the movie
                total_num_uniq_movies += 1
        # Close the file
        file.close()
        return dir_full_name, list(movie_names), total_num_uniq_movies

def get_average_degree_for_all_directors(G):
    # Get all directors in graph G
    dirs = [person for person in G.nodes if 'director' in G.nodes[person]]
    # Make a list of all directors degrees
    dir_degrees = [G.degree(dir) for dir in dirs]
    # Get the average director degree
    dirs_avg_degree = sum(dir_degrees)/len(dir_degrees)
    print("All Directors Avg. Degree (excluding crew): " + str(round(dirs_avg_degree, 4)))

def get_average_degree_for_minority_directors(G): 
    # Get all directors in graph G
    dirs = [person for person in G.nodes if 'director' in G.nodes[person]]
    # Filter out non-minority dirs
    min_dirs = [dir for dir in dirs if G.nodes[dir]['custlabel'] != 'MWH' and G.nodes[dir]['custlabel'] != 'MW']
    # Make a list of all directors degrees
    dir_degrees = [G.degree(min_dir) for min_dir in min_dirs]
    # Get the average director degree
    dirs_avg_degree = sum(dir_degrees)/len(dir_degrees)
    print("Minority Directors Avg. Degree (excluding crew): " + str(round(dirs_avg_degree, 4)))

def get_average_degree_for_renowned_directors(G):
    # Get all directors in graph G
    dirs = [person for person in G.nodes if 'director' in G.nodes[person]]
    # Filter out non-minority dirs
    rnwd_dirs = [dir for dir in dirs if "H" in G.nodes[dir]['custlabel']]
    # Make a list of all directors degrees
    dir_degrees = [G.degree(rnwd_dir) for rnwd_dir in rnwd_dirs]
    # Get the average director degree
    dirs_avg_degree = sum(dir_degrees)/len(dir_degrees)
    print("Renowned Directors Avg. Degree (excluding crew): " + str(round(dirs_avg_degree, 4)))

# Gets all opportunites for each role under each director
def get_total_opportunites(G):
    # Get directors in graph
    dirs = [person for person in G.nodes if 'director' in G.nodes[person]]
    dirs_role_count = {}
    for dir in dirs:
        # Keep track of total opportunities under each role
        role_count = {}
        # Go through crew working under director
        for crew_mem in G.neighbors(dir):
            # Get the crew member role and the number of times they have worked with the director (weight)
            crew_mem_role = G.nodes[crew_mem]['role']
            crew_og_weight = G.get_edge_data(dir,crew_mem)['weight']
            # If their role is in the final dictionary, add their weight to the current opportunities count
            if crew_mem_role in role_count.keys():
                role_count[crew_mem_role] += crew_og_weight
            # If their role is not in the final dictionary, add the role with value being the weight of director, crew member edge
            else:
                role_count[crew_mem_role] = crew_og_weight
        dirs_role_count[dir] = role_count
    # Return the opportunity role count dictionary
    return dirs_role_count

# Gets the role homogeneity of one director
def get_role_homogeneity_for_one_director(G, director, exclude_dir_conns=True):
    # Get all crew that have worked with director and if needed, exclude director-director connections
    if exclude_dir_conns!=True:
        dir_crew = list(G.neighbors(director))
    else:
        dir_crew = [crew for crew in G.neighbors(director) if 'director' not in G.nodes[crew]]
    # Make a dictionary with all crew as keys and their roles as values
    crew_role_dict = {}
    for crew in dir_crew:
        crew_role_dict[crew] = G.nodes[crew]["role"]
    # Get all the unique roles under this director
    unique_roles_under_dir = set(crew_role_dict.values())
    # For each role, calculate the normalized weights and homogeneity
    # Initialize a dictionary to collect role homogeneity per role
    role_homogeneity_dict = {}
    for role in unique_roles_under_dir:
        # Get all the crew members under one role
        unique_crew_under_role = [crew for crew, crew_role in crew_role_dict.items() if crew_role == role]
        # Initialize a dictionary to collect the normalized weights for each role
        # If there is only one crew member under a role, set the role homogeneity to 1
        if len(unique_crew_under_role) == 1:
            role_homogeneity = 1
        # If there is more than one crew member under a role, calculate the role homogeneity
        else:
             # Find the number of total spots hired for role
             num_role_spots_hired = sum([G.get_edge_data(director,member)['weight'] for member in unique_crew_under_role])
             # Find the total number of unique crew employed by the director
             total_unique_crew = len(unique_crew_under_role)
             # Find the homogeneity for the role by finding 1 - (total unique crew / number of spots hired)
             role_homogeneity_rv = total_unique_crew/num_role_spots_hired
             role_homogeneity = round((float(1) - role_homogeneity_rv),3)
        # Add the homogeneity of the role to the role homogeneity dictionary
        role_homogeneity_dict[role] = role_homogeneity
    # Sort the role homogeneity scores from highest to lowest
    role_homogeneity_dict = dict(sorted(role_homogeneity_dict.items(), key=lambda item: item[1],reverse=True))
    return role_homogeneity_dict

# Gets average role homogeneity for each director in dictionary format
# Choose to include/exclude director-director connections
def get_role_homogeneity_dict(G, exclude_dir_conns=True):
    # Get a list of the directors from csv
    director_list = [person for person in G.nodes if 'director' in G.nodes[person]]
    # Initialize a dictionary to collect all role homogeneity values for every director
    role_homogeneity_all_dirs_dict = {}
    # For each director calculate their role homogeneity
    for director in director_list:
        role_homogeneity_dict = get_role_homogeneity_for_one_director(G, director, exclude_dir_conns)
        # Add role homogeneity dictionary to respective dictionary with director as key
        role_homogeneity_all_dirs_dict[director] = role_homogeneity_dict
    return role_homogeneity_all_dirs_dict

# Get average role homogeneity for each director in dictionary format
# Choose to include/exclude director-director connections
def get_avg_role_homogeneity_dict(G, exclude_dir_conns=True):
    role_homogeneity_all_dirs_dict = get_role_homogeneity_dict(G,exclude_dir_conns)
    # Initialize a dictionary to collect all avg. role homogeneity scores
    avg_role_homogeneity_dict = {}
    # Add all avg. role homogeneity values to respective dictionary with director as key
    for director, role_reuse_values in role_homogeneity_all_dirs_dict.items():
        avg_reuse = round(sum(role_reuse_values.values())/len(role_reuse_values),3)
        avg_role_homogeneity_dict[director] = avg_reuse
    # Sort the dictionary by highest avg. role homogeneity descending
    avg_role_homogeneity_dict = dict(sorted(avg_role_homogeneity_dict.items(), key=lambda item: item[1],reverse=True))
    return avg_role_homogeneity_dict

# Prints top 3 homogeneous roles for each director, their custlabel, and their avg. homogeneity
def get_main_stats(G, top_dirs=False,exclude_dir_conns=True):
    rh_all_dirs_dict = get_role_homogeneity_dict(G,exclude_dir_conns)
    arh_all_dirs_dict = get_avg_role_homogeneity_dict(G, exclude_dir_conns)
    print('')
    print("Name | Attributes | Avg. Role Homogeneity | Top 3 Homogeneous Roles")
    print('-----')
    numbered = 1
    for dir, arh in arh_all_dirs_dict.items():
        # Get all director attributes
        attr = G.nodes[dir]['custlabel']
        # Get avg. role homogeneity
        arh = arh_all_dirs_dict[dir]
        # Get top 3 homogeneous roles
        top_3 = list(rh_all_dirs_dict[dir].keys())[:3]
        print(F"{numbered}. {dir} | {attr} | {arh} | {top_3[0]}, {top_3[1]}, {top_3[2]}")
        print('')
        if top_dirs is True and numbered == 10:
            break
        numbered += 1

# Gets main stats into a csv file for graph creation
def main_stats_to_csv(G, exclude_dir_conns=True):
    stats_df = pd.DataFrame()
    rh_all_dirs_dict = get_role_homogeneity_dict(G,exclude_dir_conns)
    arh_all_dirs_dict = get_avg_role_homogeneity_dict(G, exclude_dir_conns)
    for dir, arh in arh_all_dirs_dict.items():
        label = G.nodes[dir]['custlabel']
        top_roles = list(rh_all_dirs_dict[dir].keys())[:3]
        top_3 = F"{top_roles[0]}, {top_roles[1]}, {top_roles[2]}"
        dir_info = {"name":dir, "custlabel": label, "arh": arh, "top_3":top_3, "role1":top_roles[0],"role2":top_roles[1], "role3": top_roles[2]}
        stats_df = stats_df.append(dir_info, ignore_index=True)
    stats_df.to_csv("main_stats.csv")
    print("Wrote main_stats.csv..")

def get_dir_clustering_coefs(G):
    dirs = [person for person in G.nodes if 'director' in G.nodes[person]]
    clust_coef = {}
    print('')
    for dir in dirs:
        clust_coef[dir] = round(nx.clustering(G,dir), 6)
    clust_coef = dict(sorted(clust_coef.items(), key=lambda item: item[1],reverse=True))
    print("Director Name | Attributes | Clustering Coefficient")
    print("---")
    for dir, cc in clust_coef.items():
        attr = G.nodes[dir]['custlabel']
        print(F"{dir} | {attr} | {cc}")


# Print role homogeneity for every director or any given director when given respective dictionary
def pretty_print_get_role_homogeneity(role_homogeneity_all_dirs_dict, director=None):
    print('')
    if director != None:
        role_reuse_values = role_homogeneity_all_dirs_dict[director]
        print("Role Homogeneity for " + director)
        print('---')
        for role, reuse_values in role_reuse_values.items():
            print(role + ': ' + str(reuse_values))
    else:
        for director,role_reuse_values in role_homogeneity_all_dirs_dict.items():
            print("Role Homogeneity for " + director)
            print('---')
            for role, reuse_values in role_reuse_values.items():
                print(role + ': ' + str(reuse_values))
            print('')
    print('')

# Print the avg. role homogeneity for every director or any given director when given respective dictionary
def pretty_print_get_avg_role_homogeneity(avg_role_homogeneity_dict, director=None):
    print('')
    if director is not None:
        print(director + ' Avg. Role Homogeneity: ' + str(avg_role_homogeneity_dict[director]))
    else:
        print("Director Avg. Role Homogeneity")
        print('---')
        for director, arh in avg_role_homogeneity_dict.items():
            print(director + ': ' + str(arh))
    print('')

def pretty_print_dict(dict):
    for key, value in dict.items():
        print(key + ":", value, "\n")

if __name__ == "__main__":
    with open('.../metadata/metadata-101.pkl', 'rb') as f:
        metadata = pickle.load(f)

    person = "J.J. Abrams"
    print("Metadata for:", person, "\n")
    pretty_print_dict(metadata[person])
from ..extraction.role_processing import convert_names
import pickle
import fileinput
import os
import json
import collections
import pandas as pd

# Get list of directors from csv file
def get_director_list(path):
    df = pd.read_csv(path, sep=',', header=0)
    return [row[1] + " " + row[0] for _, row in df.iterrows()]

# Recursively search through the directory and all subdirectories
def find_file_paths():
    i = 0
    film_directors_paths = []
    for root, dirs, files in os.walk("film-directors/"):
        for file in files:
            # Check if the file extension is ".jsonl"
            if file.endswith(".jsonl"):
                film_directors_paths.append(os.path.join(root, file))
                i += 1
    return film_directors_paths

# get list of all possible roles across all jsonl files
def find_role_names():
    file_paths = sorted(find_file_paths())
    gen_title_set = set()

    # go through each file
    for file in file_paths:
        file = fileinput.input(file)
        # go through each line in file
        for line in file:
            data = json.loads(line)
            # go through each role in the credits
            for i in range(len(data["full_credits"])):
                # grab the general title, add to set
                gen_title = data["full_credits"][i]['role']
                gen_title_set.add(gen_title)
        file.close()

    return list(gen_title_set)

# Get names and information for every individual in json file
# Returns a dictionary mapping of name and a set of roles the individual has worked
# Also returns a set of all names seen in the json object
def extract_info(data, exclusions):
    # credits_dict = collections.defaultdict(set)
    credits_dict = collections.defaultdict(list)
    names_set = set()

    for i in range(len(data["full_credits"])):
        role = data["full_credits"][i]['role']
        
        for j in range(len(data["full_credits"][i]['crew'])):
            person = data["full_credits"][i]['crew'][j]['name']
            # check the role and convert to general title, return None if we want to skip
            gen_role = convert_names(role, exclusions)
            if gen_role != None:
                credits_dict[person].append(gen_role)
                names_set.add(person)
        
    return credits_dict, names_set

if __name__ == "__main__":
    gen_title_set = find_role_names()
    for item in gen_title_set:
        print(item)
    print(len(gen_title_set))

    print("\n")
    for item in set([convert_names(item) for item in gen_title_set]):
        print(item)
    print(len(set([convert_names(item) for item in gen_title_set])))
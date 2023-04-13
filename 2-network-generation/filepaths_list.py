import fileinput
import os
import json

# Recursively search through the directory and all subdirectories
def find_file_paths():
    i = 0
    film_directors_paths = []
    for root, dirs, files in os.walk("../1-data-extraction/"):
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


if __name__ == "__main__":
    gen_title_set = find_role_names()
    print(gen_title_set)
    print(len(gen_title_set))
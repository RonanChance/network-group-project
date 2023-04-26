import pickle

# get list of all movies across all jsonl files
def find_movie_names():
    file_paths = sorted(find_file_paths())
    movie_names = []
    total_num_uniq_movies = 0
    # go through each file
    for file in file_paths:
        file = fileinput.input(file)
        # go through each line in file
        for line in file:
            data = json.loads(line)
            # grab the movie name and add it to final set
            if data['title'] not in movie_names:
                movie_names.append(data['title'])
                # count the movie
                total_num_uniq_movies += 1
        file.close()

    return list(movie_names), total_num_uniq_movies

def pretty_print_dict(dict):
    for key, value in dict.items():
        print(key + ":", value, "\n")

if __name__ == "__main__":
    with open('../2-network-generation/metadata/metadata-101.pkl', 'rb') as f:
        metadata = pickle.load(f)

    person = "Andrew Pouch"
    print("Metadata for:", person, "\n")
    #pretty_print_dict(metadata[person])
    pretty_print_dict(metadata[person])

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

# get list of all movies across all jsonl files
def find_movie_names():
    file_paths = sorted(find_file_paths())
    movie_names = set()
    total_num_movies = 0
    # go through each file
    for file in file_paths:
        file = fileinput.input(file)
        # go through each line in file
        for line in file:
            data = json.loads(line)
            # grab the movie name and add it to final set
            movie_names.add(data['title'])
            # count the movie
            total_num_movies += 1
        file.close()

    return list(movie_names), total_num_movies

if __name__ == "__main__":
    movie_names, total_num_movies = find_movie_names()
    for movie in movie_names:
        print(movie)
    print(total_num_movies)
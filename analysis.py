from functions.generation.find_info import find_file_paths
import fileinput
import os
import json

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

if __name__ == "__main__":
    movie_names, total_num_movies = find_movie_names()
    for movie in movie_names:
        print(movie)
    print(total_num_movies)
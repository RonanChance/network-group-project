from scraper_func import get_full_crew_for_movie, get_full_credits_for_director, is_feature_film
from names_dictionary import get_dict_from_csv
from time import sleep
import shutil
import json
import os

# constants to resume scraping & specify whether to overwrite
START_MIN = None
END_MAX = None
OVERWRITE = None

if __name__ == "__main__":
    '''
    Runs entire process.
    Gets a dictionary mapping of names to ID from names_dictionary.py.
    Iterates over ids, get full credits for each director.
    Check if movie is a feature film, if so write information to relevant file in subdirectory labeled by their last name
    '''

    # overwrite the directory if chosen
    if OVERWRITE:
        film_directors_path = "./film-directors"
        if os.path.exists(film_directors_path):
            shutil.rmtree(film_directors_path)
        os.makedirs(film_directors_path)

    # get a dictionary that maps director names to their ID from custom python file
    director_to_id = get_dict_from_csv("directors.csv")

    i = 0
    for key, value in director_to_id.items():
        # get the first letter of the director's last name
        first_letter_lastname = key[0]

        # only run for a certain range of directors
        if START_MIN:
            if i < START_MIN:
                i += 1
                continue
        if END_MAX:
            if i == END_MAX + 1:
                exit(0)

        # if that directory doesn't exist, make it
        if not os.path.exists("./film-directors/" + first_letter_lastname):
            os.makedirs("./film-directors/" + first_letter_lastname)
        
        # create a file for the director, open in append mode
        filename = "./film-directors/" + first_letter_lastname + "/" + str(key) + ".jsonl"
        f = open(filename, "a")

        credits = get_full_credits_for_director(value)

        for movie in credits["credits"]:
            movie_id = movie["uri"].split("/")[4]
            if is_feature_film(movie_id):
                full_crew = get_full_crew_for_movie(movie_id)
                json.dump(full_crew, f)
                f.write("\n")
                sleep(0.05)
        
        # print confirmation to user and close file
        print("Finished Director", key)
        f.close()
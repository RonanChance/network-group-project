from scraper_func import get_full_crew_for_movie, get_full_credits_for_director
from names_dictionary import get_dict_from_csv
import os
import shutil
import json

# Note - way to get just ID numbers from directors.csv:
# grep -o 'nm[0-9]\+' directors.csv | awk '{printf "\"%s\",", $0}' 

director_ids = ["nm0009190","nm0000095","nm0000759","nm0027572","nm0000777","nm0036349","nm0004716","nm0037708","nm0000876","nm0000881","nm0000941","nm0122344","nm0000318","nm0000116","nm0001005","nm0138927","nm0160840","nm0001054","nm0001060","nm3363032","nm0000338","nm0001068","nm0000343","nm0001081","nm0190859","nm0200005","nm0000361","nm0868219","nm1148550","nm0000142","nm0000386","nm0269463","nm0000399","nm0281945","nm1560977","nm0298807","nm1950086","nm0336620","nm0336695","nm0362566","nm1802161","nm0366004","nm0001331","nm0002132","nm1716636","nm0392237","nm0000165","nm0327944","nm0001392","nm0000464","nm1503575","nm0420941","nm0426059","nm0005069","nm0476201","nm1883257","nm0000490","nm0000487","nm0501435","nm0000500","nm0510912","nm0000186","nm0000517","nm0000520","nm0570912","nm0583600","nm0590122","nm0619762","nm0634240","nm0668247","nm1443502","nm1347153","nm0001631","nm0697656","nm0000600","nm2011696","nm0716980","nm0751102","nm0751577","nm0000217","nm0000631","nm1119645","nm0796117","nm0001741","nm0001752","nm0000229","nm0000231","nm0000233","nm0853380","nm0001814","nm0893659","nm0898288","nm0905154","nm0905152","nm0169806","nm1490123","nm0911061","nm1218281","nm0946734","nm0000709","nm2125482"]

# overwrite the directory if it already exists
film_directors_path = "./2-network-generation/film-directors"
if os.path.exists(film_directors_path):
    shutil.rmtree(film_directors_path)
os.makedirs(film_directors_path)

# get a dictionary that maps director names to their IDs, from my custom python file
director_to_id = get_dict_from_csv()

i = 0
for key, value in director_to_id.items():
    filename = "./2-network-generation/film-directors/" + str(key) + ".json"
    credits = get_full_credits_for_director(value)
    with open(filename, "w") as f:
        json.dump(credits, f)

    i += 1
    if i == 5:
        exit()
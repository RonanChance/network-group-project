import fileinput

def get_dict_from_csv(path):
    file = fileinput.input(path)
    line = file.readline()

    director_to_id = {}
    id_to_director = {}

    for line in file:
        line = line.strip().split(",")
        # make names by last-first and fill spaces with single dash
        name_str = str(line[0] + "-" + line[1]).replace(" ", "-").replace("--", "-")
        # get id by splitting the url
        id_str = line[-1].split("/")[4]
        director_to_id[name_str] = id_str
        id_to_director[id_str] = name_str

    return director_to_id
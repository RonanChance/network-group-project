import os

# Recursively search through the directory and all its subdirectories
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
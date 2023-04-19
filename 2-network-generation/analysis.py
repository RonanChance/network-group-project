import pickle

with open('./metadata/metadata.pkl', 'rb') as f:
    metadata = pickle.load(f)

print(metadata['J.J. Abrams'])
import json

def load_config(path):
    with open(path, 'r') as j:
        return json.load(j)
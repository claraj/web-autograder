import json

def parse(filepath, root_element=None):
    all = json.load(open(filepath))
    if root_element:
        return all['root_element']
    return all

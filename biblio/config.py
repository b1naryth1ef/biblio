import os
import json
import fnmatch


def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)


def match_path(config, path):
    name = os.path.basename(path)

    for rule in config['rules']:
        if not fnmatch.fnmatch(name, rule):
            return False

    return True

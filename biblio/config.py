import yaml
import fnmatch


def load_config(path):
    with open(path, 'r') as f:
        return yaml.load(f)


def match_path(config, path):
    for rule in config['rules']:
        if not fnmatch.fnmatch(path, rule):
            return False

    return True

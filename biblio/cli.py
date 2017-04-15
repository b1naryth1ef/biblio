import os
import argparse

from pprint import pprint

from biblio.outputs import OUTPUTS
from biblio.config import load_config, match_path
from biblio.parser.util import walk_path
from biblio.parser.walker import ast_to_dict, flatten

parser = argparse.ArgumentParser()
parser.add_argument('config', help='Path to configuration file')
parser.add_argument('--debug', help='Print raw AST', action='store_true')


def main():
    args = parser.parse_args()

    config = load_config(args.config)

    typ = OUTPUTS.get(config['output'].pop('type'))
    if not typ:
        print 'ERROR: invalid output specified'
        return

    output = typ(config['output'])
    path = os.path.join(os.path.dirname(args.config), config['path'])

    for file_path in walk_path(path):
        if not match_path(config, file_path):
            continue

        with open(file_path, 'r') as f:
            module = ast_to_dict(f.read())

        if args.debug:
            pprint(module)

        flat = flatten(module)
        module_name = file_path[:-3].replace('/', '.')
        output.output_module(module_name, flat)


if __name__ == '__main__':
    main()

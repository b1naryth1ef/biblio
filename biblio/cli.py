import os
import argparse

from pprint import pprint

from biblio.config import load_config, match_path
from biblio.parser.util import walk_path
from biblio.parser.walker import ast_to_dict, flatten
from biblio.outputs.markdown import MarkdownOutput

parser = argparse.ArgumentParser()
parser.add_argument('config', help='Path to configuration file')
parser.add_argument('--debug', help='Print raw AST', action='store_true')


def main():
    args = parser.parse_args()

    config = load_config(args.config)

    config['output'].pop('type')
    output = MarkdownOutput(config['output'])

    path = os.path.join(os.path.dirname(args.config), config['path'])

    for file_path in walk_path(path):
        if not match_path(config, file_path):
            continue

        with open(file_path, 'r') as f:
            module = ast_to_dict(f.read())

        if args.debug:
            pprint(module)

        flat = flatten(module)

        if args.debug:
            pprint(flat)

        module_name = file_path[:-3].replace('/', '.')
        output.output_module(module_name, flat)


if __name__ == '__main__':
    main()

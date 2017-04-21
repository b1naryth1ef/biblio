from __future__ import print_function

import os
import ast
import json
import time
import argparse

from biblio import Biblio
from biblio.util import walk_path
from biblio.walker import Walker
from biblio.outputs import OUTPUTS
from biblio.parsers import PARSERS
from biblio.config import load_config, match_path
from biblio.util import walk_path

parser = argparse.ArgumentParser()
parser.add_argument('config', help='Path to configuration file')
parser.add_argument('--debug', action='store_true')


def main():
    args = parser.parse_args()
    config = load_config(args.config)
    path = os.path.dirname(args.config)
    b = Biblio(path, config, debug=args.debug)
    b.run()


    '''
    # Determine and build output
    otyp = OUTPUTS.get(config['output'].pop('type'))
    if not otyp:
        print('ERROR: invalid output specified')
        return
    output = otyp(config['output'])

    # Determine and build parser
    ptyp = PARSERS.get(config.get('parser', 'numpy'))
    if not ptyp:
        print('ERROR: invalid parser specified')
        return
    doc_parser = ptyp()

    # Determine path to scan
    path = os.path.dirname(args.config)
    if 'path' in config:
        path = os.path.join(path, config['path'])

    modules = []

    print('[WALK] --- START ---')
    start = time.time()
    for file_path in walk_path(path):
        module_path = file_path.replace(os.path.commonprefix([path, file_path]) + '/', '')
        module_name = module_path[:-3].replace('/', '.')
        if not match_path(config, module_path):
            continue

        with open(file_path, 'r') as f:
            print('[WALK] {}'.format(module_name))
            module = Walker(doc_parser).visit(ast.parse(f.read()))
            modules.append((module_name, module))
    print('[WALK] --- END (%ss) ---' % (time.time() - start))

    print('[OUTPUT] --- START ---')
    start = time.time()
    output.begin(modules)
    for module_name, module in modules:
        print('[OUTPUT] {}'.format(module_name))
        output.output_module(module_name, module)
    output.complete(modules)
    print('[OUTPUT] --- END (%ss) ---' % (time.time() - start))

    if args.debug:
        with open(args.debug, 'w') as f:
            json.dump(modules, f, indent=2, sort_keys=True)
    '''

if __name__ == '__main__':
    main()

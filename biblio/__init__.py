import os
import ast
import six
import logging

from biblio.util import walk_path
from biblio.walker import Walker
from biblio.outputs import OUTPUTS
from biblio.parsers import PARSERS


logging.basicConfig(
    format='[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'
)


class Biblio(object):
    def __init__(self, path, config, debug=False):
        self.path = path
        self.config = config
        self.log = logging.getLogger(__name__)

        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

    def run(self):
        modules = self._walk()
        for output in self.config['outputs']:
            self._output(output, modules)
        pass

    def _output(self, output, modules):
        self.log.info('Running output %s on %s modules', output['type'], len(modules))

        output_type = OUTPUTS.get(output['type'])
        if not output_type:
            raise Exception('Invalid output `{}` requested'.format(output['type']))
        output = output_type(output)

        output.begin(modules)
        for name, module in modules:
            self._output_module(name, module, output)
        output.complete(modules)

    def _output_module(self, name, module, output):
        self.log.info('outputting module %s', name)
        output.output_module(name, module)

    def _walk(self):
        self.log.info('Walking %s rules', len(self.config['rules']))
        return reduce(sum, [list(self._walk_rule(*i)) for i in six.iteritems(self.config['rules'])])

    def _walk_rule(self, rule, options):
        self.log.info('Walking rule %s', rule)

        curdir = os.getcwd()
        os.chdir(self.path)

        parser_type = PARSERS.get(options.get('parser', 'numpy'))
        if not parser_type:
            raise Exception('Invalid parser `{}` requested'.format(options.get('parser')))
        doc_parser = parser_type()

        for file_path in walk_path('.', rule):
            yield self._process_file(file_path, doc_parser)

        os.chdir(curdir)

    def _process_file(self, file_path, doc_parser):
        self.log.debug('processing file %s', file_path)
        module_name = os.path.splitext(file_path)[0].replace('/', '.')
        with open(file_path, 'r') as f:
            return module_name, Walker(doc_parser).visit(ast.parse(f.read()))

import re
import sys

from jinja2 import Environment, PackageLoader

from ..base import BaseOutput

REFERENCE_RE = re.compile(r'`(\w[^`]+)`')


class MarkdownOutput(BaseOutput):
    def __init__(self, *args, **kwargs):
        self.process_references = kwargs.pop('process_references', True)
        super(MarkdownOutput, self).__init__(*args, **kwargs)
        self.env = Environment(
            loader=PackageLoader('biblio', 'outputs/markdown/templates/'))
        self.env.filters['clean'] = lambda s: s.replace('\n', ' ').replace('|', '&#124;').replace('`', '&#96;')
        self.env.filters['pdoc'] = self.process_docstring

        self.classes = {}
        self.classes_full = {}

    def process_docstring(self, docstring):
        def _f(match):
            match = match.group(1)
            if match in self.classes:
                obj = self.classes[match]
            elif match in self.classes_full:
                obj = self.classes_full[match]
            else:
                return '`{}`'.format(match)

            return '[`{}`]({}.html#{})'.format(
                match,
                obj[0].replace('.', '_'),
                obj[1]['name'].lower(),
            )

        if self.process_references:
            return REFERENCE_RE.sub(_f, docstring)

        return docstring

    def process_module(self, name, module):
        print name
        for cls in module['classes']:
            if cls['name'] in self.classes:
                del self.classes[cls['name']]
            else:
                self.classes[cls['name']] = (name, cls)

            full = name + '.' + cls['name']
            if full in self.classes_full:
                del self.classes_full[full]
            else:
                self.classes_full[full] = (name, cls)

    def output_module(self, name, module):
        with open(self.module_path(name, 'md'), 'w') as f:
            template = self.env.get_template('module.md')
            data = template.render(module=module, name=name)

            if (sys.version_info > (3, 0)):
                f.write(data)
            else:
                f.write(data.encode('utf-8'))

    def begin(self, modules):
        self.modules = modules

        for name, module in modules:
            self.process_module(name, module)

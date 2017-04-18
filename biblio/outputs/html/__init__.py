from __future__ import print_function

import os
import re
import sys

from jinja2 import Environment, FileSystemLoader

from ..base import BaseOutput


REFERENCE_RE = re.compile(r'`(\w[^`]+)`')


class HTMLOutput(BaseOutput):
    def __init__(self, *args, **kwargs):
        super(HTMLOutput, self).__init__(*args, **kwargs)
        default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
        self.env = Environment(
            loader=FileSystemLoader(self.config.get('template_path', default_path)))
        self.env.filters['heading'] = self.heading
        self.env.filters['pdoc'] = self.process_docstring

        self.classes = {}
        self.classes_full = {}

    @staticmethod
    def heading(level):
        return 'h{}'.format(level)

    def process_docstring(self, docstring):
        def _f(match):
            match = match.group(1)
            if match in self.classes:
                obj = self.classes[match]
            elif match in self.classes_full:
                obj = self.classes_full[match]
            else:
                print('[WARNING] unresolved reference `{}`'.format(match))
                return match
            return '<a href="/{}.html#{}">{}</a>'.format(
                obj[0].replace('.', '_'),
                obj[1]['name'],
                match
            )

        return REFERENCE_RE.sub(_f, docstring)

    def output_module(self, name, module):
        with open(self.module_path(name, 'html'), 'w') as f:
            template = self.env.get_template('module.html')
            data = template.render(module=module, name=name)

            if (sys.version_info > (3, 0)):
                f.write(data)
            else:
                f.write(data.encode('utf-8'))

    def process_module(self, name, module):
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

    def begin(self, modules):
        for name, module in modules:
            self.process_module(name, module)

    def complete(self, modules):
        with open(os.path.join(self.path, 'index.html'), 'w') as f:
            f.write(self.env.get_template('index.html').render(modules=modules))

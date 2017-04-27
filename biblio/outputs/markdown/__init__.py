import os
import sys

from jinja2 import Environment, FileSystemLoader

from ..base import BaseOutput


class MarkdownOutput(BaseOutput):
    def __init__(self, *args, **kwargs):
        super(MarkdownOutput, self).__init__(*args, **kwargs)
        default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
        self.env = Environment(
            loader=FileSystemLoader(self.config.get('template_path', default_path)))
        self.env.filters['clean'] = lambda s: s.replace('\n', ' ').replace('|', '&#124;').replace('`', '&#96;')

    def process_docstring(self, docstring):
        return docstring

    def output_module(self, name, module):
        with open(self.module_path(name, 'md'), 'w') as f:
            template = self.env.get_template('module.md')
            data = template.render(module=module, name=name)

            if (sys.version_info > (3, 0)):
                f.write(data)
            else:
                f.write(data.encode('utf-8'))

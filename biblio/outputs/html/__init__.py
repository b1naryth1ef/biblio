import os

from jinja2 import Environment, FileSystemLoader

from ..base import BaseOutput


class HTMLOutput(BaseOutput):
    def __init__(self, *args, **kwargs):
        super(HTMLOutput, self).__init__(*args, **kwargs)
        default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
        self.env = Environment(
            loader=FileSystemLoader(self.config.get('template_path', default_path)))

        with open(os.path.join(self.path, 'index.html'), 'w') as f:
            f.write(self.env.get_template('index.html').render())

    def output_module(self, name, module):
        with open(self.module_path(name, 'html'), 'w') as f:
            f.write(self.env.get_template('module.html').render(module=module, name=name))

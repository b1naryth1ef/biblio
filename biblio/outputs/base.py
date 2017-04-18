import os


class BaseOutput(object):
    def __init__(self, config):
        self.config = config
        self.index = {}

        if 'path' in config:
            self.path = config['path']

        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def module_path(self, module, ext):
        return os.path.join(self.path, module.replace('.', '_') + '.' + ext)

    def output_module(self, name, module):
        return None

    def begin(self, modules):
        pass

    def complete(self, modules):
        pass

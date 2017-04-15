from __future__ import absolute_import

import json
from .base import BaseOutput


class JSONOutput(BaseOutput):
    def output_module(self, name, module):
        with open(self.module_path(name, 'json'), 'w') as f:
            json.dump(module, f, indent=2, sort_keys=True)

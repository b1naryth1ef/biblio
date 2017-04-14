import os

from jinja2 import Template

TEMPLATE = """
# {{ name }}

{{ module['docs'] or '' }}

{% if module['classes'] %}
## Classes

{% for class in module['classes'] %}
### {{ class['name'] }}

{{ class['docs'] or '' }}

{% if class['attributes'] %}
#### Attributes

{% for attr in class['attributes'] %}
`{{ attr['name'] }}`
{% endfor %}
{% endif %}

{% if class['functions'] %}
#### Functions

{% for func in class['functions'] %}
##### {{ func['name'] }}({{ func['args']|join(', ') }})

{{ func['docs'] or '' }}
{% endfor %}
{% endif %}

{% endfor %}
{% endif %}
"""


class MarkdownOutput(object):
    def __init__(self, config):
        self.path = config['path']

        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def output_module(self, name, module):
        template = Template(TEMPLATE)
        data = template.render(name=name, module=module)

        name = name.replace('.', '_')
        with open(os.path.join(self.path, name + '.md'), 'w') as f:
            f.write(data)

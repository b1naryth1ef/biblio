# {{ name }}

{% if module['docstring'] %}
{% set docstring = module['docstring'] %}
{% include 'docstring.md' %}
{% endif %}

{% if module['variables'] %}
## Constants
{% for constant in module['variables'] %}
{% include 'constant.md' %}
{% endfor %}
{% endif %}

{% if module['classes'] %}
## Classes
{% for class in module['classes'] %}
{% include 'class.md' %}
{% endfor %}
{% endif %}

{% if module['functions'] %}
## Functions
{% for function in module['functions'] %}
{% include 'function.md' %}
{% endfor %}
{% endif %}

### {{ class["name"] }}

{% if class["bases"] %}
_Inherits From {% for base in class['bases'] %}`{{ base['name'] }}`
{%- if not loop.last %}, {% endif %}{% endfor %}_
{% endif %}

{% if class['docstring'] %}
{% set docstring = class['docstring'] %}
{% include 'docstring.md' %}
{% endif %}

{% if class['functions'] %}
#### Functions
{% for function in class['functions'] %}
{% include 'function.md' %}
{% endfor %}
{% endif %}

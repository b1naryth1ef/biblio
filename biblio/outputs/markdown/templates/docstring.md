{%- if docstring['sections']['header'] -%}
{%- for content in docstring['sections']['header'] -%}
{{ content['content'] }}
{%- endfor -%}
{%- endif -%}

{% for section, data in docstring['sections'].items() %}
{% if section != 'header' and section not in ('returns', 'yields', 'raises') %}
##### {{ section|title }}

| Name | Type | Description |
|------|------|-------------|
{%- for entry in data %}
| {{ entry['name']|clean }} | {% if entry['type'] %}<code>{{ entry['type']|clean }}</code>{% endif %} | {{ entry['content']|clean }} |
{%- endfor -%}
{% elif section != 'header' %}
##### {{ section|title }}

{% for entry in data %}
{{ entry['content'] }}
{% endfor %}
{%- endif -%}
{%- endfor -%}

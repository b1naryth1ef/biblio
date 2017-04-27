{% if constant['value']['type'] == 'call' %}
```python
{{ constant['targets'][0] }} = {% if constant['value']['name']['name'] -%}
  {{ constant['value']['name']['name'] }}
{%- else -%}
  {{ constant['value']['name'] }}
{%- endif %}(
  {%- if constant['value']['keywords'] -%}
  {%- for kw in constant['value']['keywords'] %}
  {{ kw['arg'] }} = {{ kw['value'] }}{% if not loop.last %},{% endif %}
  {%- endfor -%}
  {%- elif constant['value']['args'] -%}
  {{ constant['value']['args']|join(', ') }}
  {%- endif %})
```
{% else %}
{{ constant }}
{% endif %}

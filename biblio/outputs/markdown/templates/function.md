{% macro func_var(var) -%}
{% if var['type'] -%}
{{ var['elts'] }}
{%- else -%}
{{ var }}
{%- endif %}
{%- endmacro %}

#### {{ function['name'] }}(
{%- for arg in function['args']['args'] -%}<code>
{%- if function['args']['defaults']|length > loop.revindex -%}
{{ arg }}={{ func_var(function['args']['defaults'][-loop.revindex]) }}
{%- else -%}
{{ arg }}
{%- endif -%}
{%- if not loop.last %}, {% endif %}
{%- endfor -%}
{%- if function['args']['vargs'] -%}
{%- if function['args']['args'] -%},{%- endif -%}
\*{{ function['args']['vargs'] }}
{%- endif -%}
{%- if function['args']['kwargs'] -%}
{%- if function['args']['args'] or function['args']['vargs'] -%},{%- endif -%}
\*\*{{ function['args']['kwargs'] }}
{%- endif -%}
</code>)

{% if function['docstring'] %}
{% set docstring = function['docstring'] %}
{% include 'docstring.md' %}
{% endif %}

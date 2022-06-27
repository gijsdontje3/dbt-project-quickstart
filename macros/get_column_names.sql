{% macro get_column_names(datasource) %}

{%- 
set relation = api.Relation.create(
    database = target.database,
    schema = datasource.schema,
    identifier = datasource.identifier
)
-%}

{%- set columns = [] -%}

{%- for col in adapter.get_columns_in_relation(relation) -%}
{%- set columns = columns.append(col.name) -%}
{%- endfor -%}

{{ return(columns) }}

{% endmacro %}

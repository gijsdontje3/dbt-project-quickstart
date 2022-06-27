{% macro get_column_values(desired_column, datasource) %}

{% set some_query %}
select distinct
{{ desired_column }}
from {{ datasource }}
order by 1
{% endset %}

{% set results = run_query(some_query) %}

{% if execute %}
{% set results_list = results.columns[0].values() %}
{% else %}
{% set results_list = [] %}
{% endif %}

{{ return(results_list) }}

{% endmacro %}

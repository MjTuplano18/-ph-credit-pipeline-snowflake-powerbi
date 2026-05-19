-- FILE: generate_schema_name.sql
-- PURPOSE: Use custom schemas (STAGING, MART) without prefixing target schema
-- PHASE: 4
-- DEPENDS ON: dbt project configuration
-- OUTPUTS: Schema name resolution for dbt models

{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name }}
    {%- endif -%}
{%- endmacro %}

-- FILE: stg_bsp_rates.sql
-- PURPOSE: Clean and type macro data for joins with loans
-- PHASE: 4
-- DEPENDS ON: RAW.RAW_BSP_RATES
-- OUTPUTS: STAGING.STG_BSP_RATES view

with source as (
    select *
    from {{ source('raw', 'raw_bsp_rates') }}
)

select
    rate_period,
    to_date(rate_period || '-01-01') as rate_date, -- Annual series to date
    date_trunc('quarter', to_date(rate_period || '-01-01')) as rate_quarter, -- Align to loan_quarter
    policy_rate::float as policy_rate,
    inflation_rate::float as inflation_rate,
    ingested_at
from source
where inflation_rate is not null

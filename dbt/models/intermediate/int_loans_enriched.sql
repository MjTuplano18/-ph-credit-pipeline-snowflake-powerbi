-- FILE: int_loans_enriched.sql
-- PURPOSE: Enrich loans with macro indicators
-- PHASE: 4
-- DEPENDS ON: stg_loans, stg_bsp_rates
-- OUTPUTS: INTERMEDIATE.INT_LOANS_ENRICHED view

with loans as (
    select *
    from {{ ref('stg_loans') }}
),

rates as (
    select *
    from {{ ref('stg_bsp_rates') }}
)

select
    loans.*,
    rates.policy_rate,
    rates.inflation_rate
from loans
left join rates
    on loans.loan_quarter = rates.rate_quarter

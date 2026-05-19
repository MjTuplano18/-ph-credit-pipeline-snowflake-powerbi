-- FILE: mart_default_risk.sql
-- PURPOSE: Aggregate default risk metrics by loan segment
-- PHASE: 4
-- DEPENDS ON: int_loans_enriched
-- OUTPUTS: MART.MART_DEFAULT_RISK table

with base as (
    select
        loan_grade,
        loan_sub_grade,
        loan_status,
        loan_amount,
        interest_rate_pct,
        debt_to_income,
        policy_rate,
        inflation_rate
    from {{ ref('int_loans_enriched') }}
),

scored as (
    select
        *,
        case
            when loan_status in ('Charged Off', 'Default') then 1
            else 0
        end as default_flag -- Simple default definition for the mart
    from base
)

select
    loan_grade,
    loan_sub_grade,
    count(*) as loan_count,
    avg(loan_amount) as avg_loan_amount,
    avg(interest_rate_pct) as avg_interest_rate_pct,
    avg(debt_to_income) as avg_debt_to_income,
    avg(policy_rate) as avg_policy_rate,
    avg(inflation_rate) as avg_inflation_rate,
    avg(default_flag) as default_rate
from scored
group by loan_grade, loan_sub_grade

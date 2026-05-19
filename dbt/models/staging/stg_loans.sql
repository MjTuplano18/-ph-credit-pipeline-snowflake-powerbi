-- FILE: stg_loans.sql
-- PURPOSE: Clean and type raw loan data for downstream joins
-- PHASE: 4
-- DEPENDS ON: RAW.RAW_LOANS
-- OUTPUTS: STAGING.STG_LOANS view

with source as (
    select *
    from {{ source('raw', 'raw_loans') }}
),

typed as (
    select
        coalesce(
            nullif(id::string, ''),
            nullif(member_id::string, ''),
            md5(
                coalesce(loan_amnt::string, '') || '|' ||
                coalesce(term, '') || '|' ||
                coalesce(int_rate, '') || '|' ||
                coalesce(grade, '') || '|' ||
                coalesce(sub_grade, '') || '|' ||
                coalesce(emp_length, '') || '|' ||
                coalesce(home_ownership, '') || '|' ||
                coalesce(annual_inc::string, '') || '|' ||
                coalesce(issue_d, '') || '|' ||
                coalesce(purpose, '') || '|' ||
                coalesce(addr_state, '') || '|' ||
                coalesce(zip_code, '') || '|' ||
                coalesce(loan_status, '') || '|' ||
                coalesce(dti::string, '')
            )
        ) as loan_id,
        loan_amnt::number as loan_amount,
        term as loan_term,
        replace(int_rate, '%', '')::float as interest_rate_pct, -- Strip percent sign
        grade as loan_grade,
        sub_grade as loan_sub_grade,
        emp_length as employment_length,
        home_ownership,
        annual_inc::float as annual_income,
        to_date(issue_d, 'Mon-YYYY') as issue_date, -- Convert Lending Club month-year
        date_trunc('quarter', to_date(issue_d, 'Mon-YYYY')) as loan_quarter, -- Align with macro data
        loan_status,
        dti::float as debt_to_income,
        ingested_at
    from source
)

select *
from typed

-- FILE: mart_collections_priority.sql
-- PURPOSE: Rank loan segments for collections follow-up
-- PHASE: 4
-- DEPENDS ON: mart_default_risk
-- OUTPUTS: MART.MART_COLLECTIONS_PRIORITY table

select
    loan_grade,
    loan_sub_grade,
    loan_count,
    avg_loan_amount,
    default_rate,
    (default_rate * avg_loan_amount) as priority_score -- Higher score means higher collections priority
from {{ ref('mart_default_risk') }}
order by priority_score desc

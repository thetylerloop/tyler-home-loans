#!/usr/bin/env python

import agate


table = agate.Table.from_csv('data/hmda_lar__smith_county__all_years__filtered.csv', column_types={
    'census_tract_number_string': agate.Text()
})

grouped = table.group_by('census_tract_number_string')

summarized = grouped.aggregate([
    ('count', agate.Count()),
    ('avg_applicant_income_000s', agate.Mean('applicant_income_000s')),
    ('avg_loan_amount_000s', agate.Mean('loan_amount_000s'))
])

summarized.to_csv('data/census_tract_summary.csv')
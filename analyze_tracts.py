#!/usr/bin/env python

import pandas
import geopandas


filtered_data = pandas.read_csv('data/hmda_lar__smith_county__all_years__filtered.csv', dtype={
    'census_tract_number_string': str
})

tract_data = filtered_data.groupby('census_tract_number_string', as_index=False).agg({
    'state_name': 'count',
    'applicant_income_000s': 'mean',
    'loan_amount_000s': 'mean'
})

tract_data = tract_data.rename(index=str, columns={
    'census_tract_number_string': 'TRACTCE',
    'state_name': 'applicant_count',
    'applicant_income_000s': 'avg_applicant_income_000s',
    'loan_amount_000s': 'avg_loan_amount_000s'
})

tracts = geopandas.read_file('data/tl_2017_48_tract')

tracts = tracts.merge(tract_data, on='TRACTCE')

tracts.to_file('data/merged_tracts/merged_tracts.shp')
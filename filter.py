#!/usr/bin/env python

import csv
import math


output = []


with open('data/hmda_lar__smith_county__all_years.csv') as f:
    reader = csv.DictReader(f)

    for row in reader:
        if row['loan_type_name'] != 'Conventional':
            continue

        if row['property_type_name'] != 'One-to-four family dwelling (other than manufactured housing)':
            continue

        if row['owner_occupancy_name'] != 'Owner-occupied as a principal dwelling':
            continue

        if row['loan_purpose_name'] != 'Home purchase':
            continue

        if row['action_taken_name'] not in ['Loan originated', 'Application denied by financial institution']:
            continue

        if row['loan_amount_000s']:
            loan_amount = int(row['loan_amount_000s'])

            if loan_amount >= 90000:
                continue
            else:
                row['log_loan_amount_000s'] = math.log(loan_amount)
        else:
            row['log_loan_amount_000s'] = None

        if row['applicant_income_000s']:
            income = int(row['applicant_income_000s'])

            if income == 9999:
                continue
            else:
                row['log_applicant_income_000s'] = math.log(income)
        else:
            row['log_applicant_income_000s'] = None

        if row['applicant_ethnicity_name'] == 'Hispanic or Latino':
            row['race_ethnicity'] = 'Hispanic or Latino'
        elif row['applicant_ethnicity_name'] == 'Not Hispanic or Latino':
            if row['applicant_race_name_1'] == 'White':
                row['race_ethnicity'] = 'White'
            elif row['applicant_race_name_1'] == 'Black or African American':
                row['race_ethnicity'] = 'Black or African American'
            elif row['applicant_race_name_1'] == 'Asian':
                row['race_ethnicity'] = 'Asian'
            else:
                row['race_ethnicity'] = 'Other or N/A'
        else:
            row['race_ethnicity'] = 'Other or N/A'

        row['census_tract_number_string'] = row['census_tract_number'].replace('.', '')

        output.append(row)


with open('data/hmda_lar__smith_county__all_years__filtered.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames + [
        'log_loan_amount_000s',
        'log_applicant_income_000s',
        'race_ethnicity',
        'census_tract_number_string'
    ])
    writer.writeheader()

    for row in output:
        writer.writerow(row)
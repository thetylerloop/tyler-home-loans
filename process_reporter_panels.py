#!/usr/bin/env python

import csv
from functools import partial
import string


AGENCY_CODE_TO_ABBR = {
    '1': 'OCC',
    '2': 'FRS',
    '3': 'FDIC',
    '4': 'OTS',
    '5': 'NCUA',
    '7': 'HUD',
    '8': '?',
    '9': 'CFPB'
}


output = {}
processed_ids = []

for filename in ['Panel.final.2010.dat']:
    with open(f'data/panels/{filename}') as f:
        for line in f:
            agency_code = line[15:16]
            agency_abbr = AGENCY_CODE_TO_ABBR[agency_code]
            respondent_id = line[0:10]

            output[(agency_code, respondent_id)] = {
                'agency_abbr': agency_abbr,
                'respondent_id': respondent_id,
                'respondent_name': line[18:48].strip(),
                'total_assets': line[77:87],
                'parent_id': line[88:98].strip(),
                'parent_name': line[98:128].strip()
            }

for filename in ['2016HMDAReporterPanel.dat']:
    with open(f'data/panels/{filename}') as f:
        for line in f:
            agency_code = line[14:15]
            agency_abbr = AGENCY_CODE_TO_ABBR[agency_code]
            respondent_id = line[4:14]

            output[(agency_code, respondent_id)] = {
                'agency_abbr': agency_abbr,
                'respondent_id': respondent_id,
                'respondent_name': line[95:125].strip(),
                'total_assets': line[84:94],
                'parent_id': line[15:25].strip(),
                'parent_name': line[25:55].strip()
            }

with open('data/processed_reporter_panels.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'agency_abbr', 'respondent_id', 'respondent_name', 'total_assets', 'parent_id', 'parent_name'
    ])
    writer.writeheader()

    for row in output.values():
        writer.writerow(row)

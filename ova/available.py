#!/usr/bin/env python3

from datetime import date, timedelta
import json
import logging

import requests
import pkg_resources

log = logging.getLogger(__name__)

LOCATIONS = pkg_resources.resource_filename('ova', 'locations.json')

with open(LOCATIONS) as f:
    locations = json.load(f)


def get_next_available(location='Ottawa City Hall', dose=1):
    location_id = locations[location]
    
    url = f'https://api.covaxonbooking.ca/public/locations/{location_id}/availability'

    headers = {'content-type': 'application/json;charset=UTF-8'}

    data = {
        'startDate': date.today().isoformat(),
        'endDate': (date.today() + timedelta(days=30)).isoformat(),
        'vaccineData': 'WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==',
        'doseNumber': dose,
        'url': 'https://vaccine.covaxonbooking.ca/manage/appointment-select'
    }

    try:
        log.info(f'Fetching available dates for: {location}.')
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_json = response.json()
    except Exception as e:
        log.error(f'Failed to fetch availabe dates for: {location}. Error: {e}.')

    for avail in response_json['availability']:
        if avail['available']:
            return {'location': location, 'next_available': avail['date']}


if __name__ == "__main__":
    for loc in locations:
        next_avail = get_next_available(location=loc)
        log.info(next_avail)

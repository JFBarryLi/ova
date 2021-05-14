#!/usr/bin/env python3

from datetime import date, timedelta
import json

import requests

LOCATIONS = {
    'ott-city-hall': 'a0h4t0000006QtbAAE'
}


def get_next_available(location=LOCATIONS['ott-city-hall']):
    url = f'https://api.covaxonbooking.ca/public/locations/{location}/availability'

    headers = {'content-type': 'application/json;charset=UTF-8'}

    data = {
        'startDate': date.today().isoformat(),
        'endDate': (date.today() + timedelta(days=30)).isoformat(),
        'vaccineData': 'WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==',
        'doseNumber': 1,
        'url': 'https://vaccine.covaxonbooking.ca/manage/appointment-select'
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    response_json = response.json()

    for avail in response_json['availability']:
        if avail['available']:
            return avail['date']
    return 'No available slot in the next 30 days.'


if __name__ == "__main__":
    next_avail = get_next_available()
    print(next_avail)

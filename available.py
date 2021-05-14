#!/usr/bin/env python3

from datetime import date, timedelta
import json

import requests

with open('locations.json') as f:
    locations = json.load(f)


def get_next_available(location=locations['Ottawa City Hall'], dose=1):
    url = f'https://api.covaxonbooking.ca/public/locations/{location}/availability'

    headers = {'content-type': 'application/json;charset=UTF-8'}

    data = {
        'startDate': date.today().isoformat(),
        'endDate': (date.today() + timedelta(days=30)).isoformat(),
        'vaccineData': 'WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==',
        'doseNumber': dose,
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

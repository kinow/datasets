#!/usr/bin/env python

import json, base64
# requests library to download and authenticate
from requests.auth import HTTPBasicAuth
from requests import get

from pprint import pprint

import math

def get_data(page):
    offset = page * 20
    url = 'http://api.eventfinda.co.nz/v2/events.json?rows=20&start_date=2016-07-30&end_date=2016-09-01&location_slug=christchurch-city&fields=event:(url,name,description,datetime_start,datetime_end,location_summary,address,is_free,point,category)&offset=%d' % offset
    print(offset)
    username = '';
    password = '';
    response = get(url, auth=HTTPBasicAuth(username, password))
    data = response.json()
    return data

def main():
    events = []

    per_page = 20
    max_page = 40
    current_page = 0

    while current_page < max_page:
        print("--- Page %d ---" % current_page)
        d = get_data(current_page)
        events.extend(d['events'])
        count = int(d['@attributes']['count'])
        last_page = math.ceil(float(count / per_page))

        current_page += 1

        if current_page == last_page:
            break

    with open('./events_chch_201608.json', 'w') as outfile:
        json.dump(events, outfile)

if __name__ == '__main__':
    main()

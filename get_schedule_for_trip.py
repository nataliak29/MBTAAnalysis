import json
import pandas as pd
import requests
import os
import sys


def get_schedule_for_trip(tripID):
    # access private api key
    with open('C:/Python37/MBTA/config.json') as json_data:
        # private api key
        config = json.load(json_data,)
        api_key = config['auth']['key']
    headers = {"x-api-key": api_key}

    # # create empty dataframe
    tripSchedule = pd.DataFrame(
        columns=['routeID',
                 'tripID',
                 'stopID',
                 'stopSequence',
                 'arrivalTime',
                 'departureTime'])

    # get json with routes information
    url = 'https://api-v3.mbta.com/schedules?filter%5Btrip%5D=' + str(tripID)
    response = requests.get(url, headers=headers)
    data = response.text
    js = json.loads(data)

    for i in range(len(js['data'])):

        routeID = js['data'][i]['relationships']['route']['data']['id']
        tripID = js['data'][i]['relationships']['trip']['data']['id']
        stopID = js['data'][i]['relationships']['stop']['data']['id']
        stopSequence = js['data'][i]['attributes']['stop_sequence']
        arrivalTime = js['data'][i]['attributes']['arrival_time']
        departureTime = js['data'][i]['attributes']['departure_time']

        tripSchedule.loc[len(tripSchedule)] = ([
            routeID,
            tripID,
            stopID,
            stopSequence,
            arrivalTime,
            departureTime

        ])

    return tripSchedule

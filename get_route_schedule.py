import json
import pandas as pd
import requests
import os
import sys
import urllib.request
import urllib.parse


def get_route_schedule(routeID, date, directionID=0, fromTime='01:00', toTime='23:00'):
    # directionID =0 - outbound, directionID =1 - inbound,
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
                 'date',
                 'stopID',
                 'stopSequence',
                 'arrivalTime',
                 'departureTime'])

    # get json with routes information
    params = urllib.parse.urlencode({
        "date": str(date),
        "direction_id": str(directionID),
        "route": str(routeID),
        "min_time": str(fromTime),
        "max_time": str(toTime)
    })
    url = 'https://api-v3.mbta.com/schedules?%s' % params

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
            date,
            stopID,
            stopSequence,
            arrivalTime,
            departureTime

        ])

    return tripSchedule


# sc = get_route_schedule('CR-Fairmount', '2019-07-22', 0, '06:00', '22:00')
# print(get_route_schedule('CR-Fairmount', '2019-07-22', 0, '06:00', '22:00'))
# sc.to_csv(
#     'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/sc.csv', index=False)

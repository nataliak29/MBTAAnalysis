import json
import pandas as pd
import requests
import os
import sys


def get_representative_trip(routeID):
    # access private api key
    with open('C:/Python37/MBTA/config.json') as json_data:
        # private api key
        config = json.load(json_data,)
        api_key = config['auth']['key']
    headers = {"x-api-key": api_key}

    # create empty dataframe
    routePatterns = pd.DataFrame(
        columns=['routeID', 'name', 'repesentativeTripID'])

    # get json with routes information
    url = 'https://api-v3.mbta.com/route_patterns/'
    response = requests.get(url, headers=headers)
    data = response.text
    js = json.loads(data)

    for i in range(len(js['data'])):
        try:
            # only typical trips and only outbound tripe (from the city to suburbs)
            if js['data'][i]['attributes']['typicality'] == 1 and js['data'][i]['attributes']['direction_id'] == 0 and js['data'][i]['relationships']['route']['data']['id'] == routeID:
                routeID = js['data'][i]['relationships']['route']['data']['id']
                name = js['data'][i]['attributes']['name']
                repesentativeTripID = js['data'][i]['relationships']['representative_trip']['data']['id']
                # print(routeID, name, desc)
                routePatterns.loc[len(routePatterns)] = ([
                    routeID,
                    name,
                    repesentativeTripID
                ])

        except:
            continue
    return routePatterns


# print(get_representative_trip('CR-Foxboro'))

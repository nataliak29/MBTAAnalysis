import json
import pandas as pd
import requests
import os
import sys
import re

# function gets route_ids, route description and first and last stop for all the routes of MBTA
# the function returns pandas table


def get_route_ids():
    # access private api key
    with open('C:/Python37/MBTA/config.json') as json_data:
        config = json.load(json_data,)
    api_key = config['auth']['key']  # private api key
    headers = {"x-api-key": api_key}

    # get json with routes information
    url = 'https://api-v3.mbta.com/routes'
    response = requests.get(url, headers=headers)
    data = response.text
    js = json.loads(data)

    # create empty dataframe
    routeNames = pd.DataFrame(
        columns=['routeID', 'routeType', 'fromStop', 'toStop'])

    # save data from json file into the dataframe
    for i in range(len(js['data'])):
        routeID = js['data'][i]['id']
        description = js['data'][i]['attributes']['description']
        fromStop = js['data'][i]['attributes']['direction_destinations'][1]
        toStop = js['data'][i]['attributes']['direction_destinations'][0]

        routeNames.loc[len(routeNames)] = ([
            routeID,
            description,
            fromStop,
            toStop
        ])

    return routeNames

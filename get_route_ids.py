import json
import pandas as pd
import requests
import os
import sys
import re

# function gets name names,ids and first and last stop for all the routes of MBTA
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

        # some of the routes have multiple destinations, they are recorded in the direction_destination field with "or" conjunction
        # every first stop has to be saved separately with respective last stop

        # case 1. multiple first stops, one last stop
        if ' or ' in fromStop and ' or ' not in toStop:
            orLocation = fromStop.find(' or ')

            # record 1st first stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                description,
                fromStop[0:orLocation],
                toStop
            ])

            # record 2nd first stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                description,
                fromStop[orLocation+4:],
                toStop
            ])
        # case 2. one first stops, multiple last stops
        elif ' or ' not in fromStop and ' or ' in toStop:
            orLocation = toStop.find(' or ')

            # record 1st last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                description,
                fromStop,
                toStop[0:orLocation]
            ])

            # record 2nd last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                description,
                fromStop,
                toStop[orLocation+4:]
            ])
        # case 3. multiple first stops, multiple last stops
        elif ' or ' in fromStop and ' or ' in toStop:
            orLocationFirst = fromStop.find(' or ')
            orLocationLast = toStop.find(' or ')

            # record 1st first stop and 1st last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                description,
                fromStop[0:orLocationFirst],
                toStop[0:orLocationLast]
            ])

            # record 2nd first stop and 2nd last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                description,
                fromStop[orLocationFirst+4:],
                toStop[orLocationLast+4:]
            ])

            # record 1st first stop and 2nd last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                description,
                fromStop[0:orLocationFirst],
                toStop[orLocationLast+4:]
            ])

            # record 2nd first stop and 1st last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                description,
                fromStop[orLocationFirst+4:],
                toStop[0:orLocationLast]
            ])

        # case 4. one first stop, one last stop
        else:
            routeNames.loc[len(routeNames)] = ([
                routeID,
                description,
                fromStop,
                toStop
            ])

        routeNames = routeNames[(routeNames.fromStop == 'South Station') | (
            routeNames.fromStop == 'North Station')]

    return routeNames


print(get_route_ids())

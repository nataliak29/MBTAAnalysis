import json
import pandas as pd
import requests
import os
import sys
import re

# function gets name names,ids and first and last stop for all the routes of MBTA
# the function returns pandas table


def get_routes_names():
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
        columns=['id', 'name', 'description', 'firstStop', 'lastStop'])

    # save data from json file into the dataframe
    for i in range(len(js['data'])):
        routeID = js['data'][i]['id']
        routeName = js['data'][i]['attributes']['long_name']
        description = js['data'][i]['attributes']['description']
        firstStop = js['data'][i]['attributes']['direction_destinations'][0]
        lastStop = js['data'][i]['attributes']['direction_destinations'][1]

        # some of the routes have multiple destinations, they are recorded in the direction_destination field with "or" conjunction
        # every first stop has to be saved separately with respective last stop

        # case 1. multiple first stops, one last stop
        if ' or ' in firstStop and ' or ' not in lastStop:
            orLocation = firstStop.find(' or ')

            # record 1st first stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                routeName,
                description,
                firstStop[0:orLocation],
                lastStop
            ])

            # record 2nd first stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                routeName,
                description,
                firstStop[orLocation+4:],
                lastStop
            ])
        # case 2. one first stops, multiple last stops
        elif ' or ' not in firstStop and ' or ' in lastStop:
            orLocation = lastStop.find(' or ')

            # record 1st last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                routeName,
                description,
                firstStop,
                lastStop[0:orLocation]
            ])

            # record 2nd last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                routeName,
                description,
                firstStop,
                lastStop[orLocation+4:]
            ])
        # case 3. multiple first stops, multiple last stops
        elif ' or ' in firstStop and ' or ' in lastStop:
            orLocationFirst = firstStop.find(' or ')
            orLocationLast = lastStop.find(' or ')

            # record 1st first stop and 1st last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                routeName,
                description,
                firstStop[0:orLocationFirst],
                lastStop[0:orLocationLast]
            ])

            # record 2nd first stop and 2nd last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                routeName,
                description,
                firstStop[orLocationFirst+4:],
                lastStop[orLocationLast+4:]
            ])

            # record 1st first stop and 2nd last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                routeName,
                description,
                firstStop[0:orLocationFirst],
                lastStop[orLocationLast+4:]
            ])

            # record 2nd first stop and 1st last stop
            routeNames.loc[len(routeNames)] = ([
                routeID,
                routeName,
                description,
                firstStop[orLocationFirst+4:],
                lastStop[0:orLocationLast]
            ])

        # case 4. one first stop, one last stop
        else:
            routeNames.loc[len(routeNames)] = ([
                routeID,
                routeName,
                description,
                firstStop,
                lastStop
            ])

    return routeNames


# print(get_routes_names())

import json
import pandas as pd
import requests
import os
import sys
import re

#function gets name metadata for all theo routes of MBTA
def get_routes_names():

    with open('C:/Python37/MBTA/config.json') as json_data:
        config = json.load(json_data,)
    api_key = config['auth']['key']
    headers  = {"x-api-key":api_key}
    url='https://api-v3.mbta.com/routes'
    response= requests.get(url,headers=headers)
    data=response.text
    js= json.loads(data)
    routeNames=pd.DataFrame( columns=['id','name','description','firstStop','lastStop'])

#save data from JSON file into pandas dataframe
    for i in range(len(js['data'])):
        routeID=js['data'][i]['id']
        routeName=js['data'][i]['attributes']['long_name']
        description=js['data'][i]['attributes']['description']
        firstStop=js['data'][i]['attributes']['direction_destinations'][0]
        lastStop=js['data'][i]['attributes']['direction_destinations'][1]

        if ' or ' in firstStop and ' or ' not in lastStop :
            orLocation=firstStop.find(' or ')

            routeNames.loc[len(routeNames)] = ([
                                routeID,
                                routeName,
                                description,
                                firstStop[0:orLocation],
                                lastStop
                                ])
            routeNames.loc[len(routeNames)] = ([
                                    routeID,
                                    routeName,
                                    description,
                                    firstStop[orLocation+4:],
                                    lastStop
                                ])

        elif ' or ' not in firstStop and ' or ' in lastStop :
            orLocation=lastStop.find(' or ')

            routeNames.loc[len(routeNames)] = ([
                                routeID,
                                routeName,
                                description,
                                firstStop,
                                lastStop[0:orLocation]
                                ])
            routeNames.loc[len(routeNames)] = ([
                                    routeID,
                                    routeName,
                                    description,
                                    firstStop,
                                    lastStop[orLocation+4:]
                                ])
        elif ' or ' in firstStop and ' or ' in lastStop :
            orLocationFirst=firstStop.find(' or ')
            orLocationLast=lastStop.find(' or ')

            routeNames.loc[len(routeNames)] = ([
                                routeID,
                                routeName,
                                description,
                                firstStop[0:orLocationFirst],
                                lastStop[0:orLocationLast]
                                ])
            routeNames.loc[len(routeNames)] = ([
                                    routeID,
                                    routeName,
                                    description,
                                    firstStop[orLocationFirst+4:],
                                    lastStop[orLocationLast+4:]
                                ])
            routeNames.loc[len(routeNames)] = ([
                                routeID,
                                routeName,
                                description,
                                firstStop[0:orLocationFirst],
                                lastStop[orLocationLast+4:]
                                ])
            routeNames.loc[len(routeNames)] = ([
                                    routeID,
                                    routeName,
                                    description,
                                    firstStop[orLocationFirst+4:],
                                    lastStop[0:orLocationLast]
                                ])
        else:
            routeNames.loc[len(routeNames)] = ([
                    routeID,
                    routeName,
                    description,
                    firstStop,
                    lastStop
                    ])

    return routeNames
# table=get_routes_names()
# table.to_csv('commuteRail/routes.csv')
print(get_routes_names())

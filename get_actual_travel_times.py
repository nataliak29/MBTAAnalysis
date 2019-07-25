
import json
import pandas as pd
import requests
import os
import sys
import urllib.request
import urllib.parse
import time
from datetime import datetime, timedelta, date


def get_actual_travel_times(main_from_date, main_to_date, from_time, to_time, from_stop, to_stop):

    traveltime = pd.DataFrame(
        columns=['routeID', 'fromStop', 'toStop', 'departure', 'arrival', 'actualTravelTimeMin'])

    with open('C:/Python37/MBTA/config.json') as json_data:
        config = json.load(json_data,)
    api_key = config['auth']['public_key']

    numberOfDays = int((datetime.strptime(main_to_date, "%d.%m.%Y") -
                        datetime.strptime(main_from_date, "%d.%m.%Y")).days)
    print('Retreiving travel time data for', numberOfDays, 'days...')

    for single_date in (datetime.strptime(main_from_date, "%d.%m.%Y") + timedelta(n) for n in range(numberOfDays)):
        from_date_time = datetime.strptime(
            str(str(single_date.strftime("%d.%m.%Y"))+' '+from_time), "%d.%m.%Y %H:%M:%S")
        to_date_time = datetime.strptime(
            str(str(single_date.strftime("%d.%m.%Y"))+' '+to_time), "%d.%m.%Y %H:%M:%S")

        from_date_time_epoch = int(from_date_time.timestamp())
        to_date_time_epoch = int(to_date_time.timestamp())

        params = urllib.parse.urlencode({
            "api_key": api_key,  # public api_key
            "format": 'json',
            "from_stop": from_stop,
            "to_stop":  to_stop,
            "from_datetime": from_date_time_epoch,
            "to_datetime": to_date_time_epoch
        })

        url = 'http://realtime.mbta.com/developer/api/v2.1/traveltimes?%s' % params

        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        js = json.loads(data)
        try:

            for i in range(len(js['travel_times'])):

                traveltime.loc[len(traveltime)] = ([
                    js['travel_times'][i]['route_id'],
                    from_stop,
                    to_stop,
                    time.strftime(
                        '%Y-%m-%d %H:%M:%S', time.localtime(int(js['travel_times'][i]['dep_dt']))),
                    time.strftime(
                        '%Y-%m-%d %H:%M:%S', time.localtime(int(js['travel_times'][i]['arr_dt']))),
                    float(js['travel_times'][i]['travel_time_sec'])/60,

                ])
        except:
            continue

    return traveltime

# # #
# main_from_date='10.04.2019'
# main_to_date = '21.07.2019'
# from_time='16:00:00'
# to_time='22:00:00'
# fromStop='South Station'
# toStop='Middleborough/Lakeville'
# js=get_travel_times(main_from_date,main_to_date,from_time,to_time,fromStop,toStop)
#
# print(js)

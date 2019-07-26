
import json
import pandas as pd
import requests
import os
import sys
import urllib.request
import urllib.parse
import time
from datetime import datetime, timedelta, date


def get_actual_travel_times(routeID, main_from_date, main_to_date, from_time, to_time, from_stop, to_stop):
    dateformat = '%Y-%m-%d'

    traveltime = pd.DataFrame(
        columns=['routeID', 'date', 'fromStop', 'toStop', 'departure', 'arrival', 'actualTravelTimeMin', 'benchmarkTravelTime'])

    with open('C:/Python37/MBTA/config.json') as json_data:
        config = json.load(json_data,)
    api_key = config['auth']['public_key']

    numberOfDays = int((datetime.strptime(main_to_date, dateformat) -
                        datetime.strptime(main_from_date, dateformat)).days)
    print('Retreiving travel time data for', numberOfDays, 'days...')

    for single_date in (datetime.strptime(main_from_date, dateformat) + timedelta(n) for n in range(numberOfDays)):
        from_date_time = datetime.strptime(
            str(str(single_date.strftime(dateformat))+' '+from_time), "%Y-%m-%d %H:%M:%S")
        to_date_time = datetime.strptime(
            str(str(single_date.strftime(dateformat))+' '+to_time), "%Y-%m-%d %H:%M:%S")

        from_date_time_epoch = int(from_date_time.timestamp())
        to_date_time_epoch = int(to_date_time.timestamp())

        params = urllib.parse.urlencode({
            "api_key": api_key,  # public api_key
            "format": 'json',
            "route": routeID,
            "from_stop": from_stop,
            "to_stop":  to_stop,
            "from_datetime": from_date_time_epoch,
            "to_datetime": to_date_time_epoch
        })

        url = 'http://realtime.mbta.com/developer/api/v2.1/traveltimes?%s' % params

        with urllib.request.urlopen(url) as f:
            # print(url)
            data = f.read().decode('utf-8')
        js = json.loads(data)
        try:

            for i in range(len(js['travel_times'])):

                traveltime.loc[len(traveltime)] = ([
                    js['travel_times'][i]['route_id'],
                    str(single_date.strftime("%Y-%m-%d")),
                    from_stop,
                    to_stop,
                    time.strftime(
                        '%H:%M:%S', time.localtime(int(js['travel_times'][i]['dep_dt']))),
                    time.strftime(
                        '%H:%M:%S', time.localtime(int(js['travel_times'][i]['arr_dt']))),
                    float(js['travel_times'][i]['travel_time_sec'])/60,
                    float(js['travel_times'][i]
                          ['benchmark_travel_time_sec'])/60,

                ])
        except:
            continue

    return traveltime


# # #
# main_from_date = '2019-07-22'
# main_to_date = '2019-07-24'
# from_time = '01:00:00'
# to_time = '19:00:00'
# fromStop = 'South Station'
# toStop = 'Readville'
# routeID = 'CR-Fairmount'
# # 'Haverhill'
# js = get_actual_travel_times(routeID, main_from_date, main_to_date,
#                              from_time, to_time, fromStop, toStop)
# # js.to_csv(
# #     'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/actualTraveltime.csv', index=False)
# print(js)

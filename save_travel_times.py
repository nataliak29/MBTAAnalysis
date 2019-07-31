from get_route_ids import get_route_ids
from get_actual_travel_times import get_actual_travel_times
from get_scheduled_travel_time import get_scheduled_travel_time
import pandas as pd
from datetime import datetime, timedelta, date
import time
start = time.time()

print('Retreiving route IDs for MBTA Commuter Rails...')
routes = get_route_ids()
routes = routes[routes.iloc[:, 1] == "Commuter Rail"]
now = datetime.now()
dateFormat = "%Y-%m-%d"
main_to_date = now.strftime(dateFormat)
main_from_date = str(datetime.strptime(
    main_to_date, dateFormat) - timedelta(7))[:10]
directionID = 0
actual_from_date = '2019-06-02'
actual_to_date = '2019-06-10'


scheduledTravelTime = pd.DataFrame(
    columns=['routeID', 'tripID', 'date', 'fromStop', 'toStop', 'departure', 'arrival', 'scheduledTravelTime'])
actualTravelTime = pd.DataFrame(
    columns=['routeID', 'date', 'fromStop', 'toStop', 'departure', 'arrival', 'actualTravelTimeMin', 'benchmarkTravelTime', 'delay'])

for i in range(len(routes)):
    routeID = routes.iloc[i, 0]
    try:
        scheduledTravelTime = scheduledTravelTime.append(get_scheduled_travel_time(routeID, main_from_date,
                                                                                   main_to_date))
    except:
        continue
scheduledTravelTime.reset_index(inplace=True)


stops = scheduledTravelTime[['routeID', 'fromStop',
                             'toStop']]
stops = stops.copy()
stops.drop_duplicates(inplace=True)

try:
    pd.read_csv("actualTravelTime.csv")
except:
    actualTravelTime.to_csv(r'actualTravelTime.csv',
                            index=None, mode='a')

for j in range(len(stops)):
    from_stop = stops.iloc[j, 1]
    to_stop = stops.iloc[j, 2]
    routeID = stops.iloc[j, 0]
    print('Retreiving actual travel time data from', from_stop, 'to', to_stop)
    try:

        travelTime = get_actual_travel_times(
            routeID, actual_from_date, actual_to_date, from_stop, to_stop)

        travelTime.to_csv(r'actualTravelTime.csv',
                          index=None, mode='a', header=False)

    except:
        continue

print('Done, the data is saved in actualTravelTime.csv')
print('It took', str(int(time.time() - start)/60), 'minutes')

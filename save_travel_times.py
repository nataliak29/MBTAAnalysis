from get_route_ids import get_route_ids
from get_actual_travel_times import get_actual_travel_times
from get_scheduled_travel_time import get_scheduled_travel_time
import pandas as pd
from datetime import datetime, timedelta, date

print('Retreiving route IDs for MBTA Commuter Rails...')
routes = get_route_ids()
routes = routes[routes.iloc[:, 1] == "Commuter Rail"]
routes = routes[(routes.iloc[:, 0] == "CR-Fairmount") |
                (routes.iloc[:, 0] == 'CR-Haverhill')]
print(routes)

main_from_date = '2019-07-22'
main_to_date = '2019-07-24'
from_time = '12:00'
to_time = '15:00'
# routeID = 'CR-Fairmount'
directionID = 0

scheduledTravelTime = pd.DataFrame(
    columns=['routeID', 'tripID', 'date', 'fromStop', 'toStop', 'departure', 'arrival', 'scheduledTravelTime'])
actualTravelTime = pd.DataFrame(
    columns=['routeID', 'date', 'fromStop', 'toStop', 'departure', 'arrival', 'actualTravelTimeMin', 'benchmarkTravelTime'])

for i in range(len(routes)):
    routeID = routes.iloc[i, 0]
    scheduledTravelTime = scheduledTravelTime.append(get_scheduled_travel_time(routeID, main_from_date,
                                                                               main_to_date, from_time, to_time, directionID))

print(scheduledTravelTime)

stops = scheduledTravelTime[['routeID', 'fromStop',
                             'toStop']]


for j in range(len(stops)):
    from_stop = stops.iloc[j, 1]
    to_stop = stops.iloc[j, 2]
    from_time_sec = str(from_time)+':00'
    to_time_sec = str(to_time)+':00'

    actualTravelTime = actualTravelTime.append(get_actual_travel_times(
        routeID, main_from_date, main_to_date, from_time_sec, to_time_sec, from_stop, to_stop))

print(actualTravelTime)

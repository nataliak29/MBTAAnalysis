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
# print(routes)

main_from_date = '2019-07-22'
main_to_date = '2019-07-24'
from_time = '01:00'
to_time = '23:00'
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


scheduledTravelTime.reset_index(inplace=True)
for s in range(len(scheduledTravelTime)):
    scheduledTravelTime.loc[s,
                            'departure_hour'] = str(scheduledTravelTime.loc[s, 'departure'])[:2]
    scheduledTravelTime.loc[s,
                            'departure_hour_pr'] = str(int(scheduledTravelTime.loc[s, 'departure_hour']) - 1)

scheduledTravelTime.to_csv(
    'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/scheduledTravelTime.csv', index=False)

print(scheduledTravelTime)

stops = scheduledTravelTime[['routeID', 'fromStop',
                             'toStop']]
stops = stops.copy()
stops.drop_duplicates(inplace=True)
# print(stops)
for j in range(len(stops)):
    from_stop = stops.iloc[j, 1]
    to_stop = stops.iloc[j, 2]
    routeID = stops.iloc[j, 0]
    print(from_stop, 'from; to', to_stop)
    from_time_sec = str(from_time)+':00'
    to_time_sec = str(to_time)+':00'

    actualTravelTime = actualTravelTime.append(get_actual_travel_times(
        routeID, main_from_date, main_to_date, from_time_sec, to_time_sec, from_stop, to_stop))

actualTravelTime.reset_index(inplace=True)
for a in range(len(actualTravelTime)):
    actualTravelTime.loc[a,
                         'departure_hour'] = str(actualTravelTime.loc[a, 'departure'])[:2]

print(actualTravelTime)
actualTravelTime.to_csv(
    'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/actualTravelTime.csv', index=False)


allTravelTime = actualTravelTime.merge(
    right=scheduledTravelTime, left_on=['routeID', 'date', 'benchmarkTravelTime', 'departure_hour'], right_on=['routeID', 'date', 'scheduledTravelTime', 'departure_hour'])

for at in range(len(allTravelTime)):
    allTravelTime.loc[at,
                      'time_lookup'] = (datetime.strptime(
                          allTravelTime.loc[at, 'departure_x'], '%H:%M:%S') - datetime.strptime(allTravelTime.loc[at, 'departure_y'], '%H:%M:%S')).total_seconds()

allTravelTime['min_time_lookup'] = allTravelTime.groupby(['routeID', 'date', 'departure_x', 'toStop_x'])[
    'time_lookup'].transform(min)


allTravelTime = allTravelTime[allTravelTime['min_time_lookup']
                              == allTravelTime['time_lookup']]
print(allTravelTime)


allTravelTime.to_csv(
    'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/allTravelTime.csv', index=False)

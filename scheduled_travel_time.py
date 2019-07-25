from get_route_ids import get_route_ids
from get_actual_travel_times import get_actual_travel_times
from get_representative_trip import get_representative_trip
from get_schedule_for_trip import get_schedule_for_trip
import pandas as pd
from datetime import datetime, timedelta, date

print('Retreiving route IDs for MBTA Commuter Rails...')
routes = get_route_ids()
crRoutes = routes[routes.iloc[:, 1] == "Commuter Rail"]
crRoutes = routes[(routes.iloc[:, 0] == "CR-Franklin") |
                  (routes.iloc[:, 0] == 'CR-Haverhill')]

tripSchedule = pd.DataFrame(
    columns=['routeID',
             'tripID',
             'stopID',
             'stopSequence',
             'arrivalTime',
             'departureTime'])
print('Retreiving schedules for routes...')
print(crRoutes)

for i in range(len(crRoutes)):
    routeID = crRoutes.iloc[i, 0]
    fromStop = crRoutes.iloc[i, 2]
    toStop = crRoutes.iloc[i, 3]

    try:
        print('Retreiving representative trip schedule for', routeID, '...')
        representativetripID = get_representative_trip(routeID).iloc[0, 2]
        print(representativetripID)
        representativetripSchedule = get_schedule_for_trip(
            representativetripID)
        for j in range(len(representativetripSchedule)):
            # if (representativetripSchedule.iloc[j, 2] == fromStop) | (representativetripSchedule.iloc[j, 2] == toStop):
            tripSchedule = tripSchedule.append(
                representativetripSchedule.iloc[j, :])

    except:
        continue
tripSchedule.to_csv(
    'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/tripSchedule.csv', index=False)

sheduledTraveltime = tripSchedule.merge(
    right=tripSchedule, left_on='routeID', right_on='routeID')
sheduledTraveltime = sheduledTraveltime[sheduledTraveltime.stopSequence_x <
                                        sheduledTraveltime.stopSequence_y]
sheduledTraveltime = sheduledTraveltime[[
    'routeID', 'stopID_x', 'arrivalTime_x', 'stopID_y', 'arrivalTime_y']]
sheduledTraveltime = sheduledTraveltime.rename(
    columns={'stopID_x': 'fromStop', 'stopID_y': 'toStop'})
sheduledTraveltime = sheduledTraveltime.reindex(
    columns=['routeID', 'fromStop', 'toStop', 'arrivalTime_x', 'arrivalTime_y'])


sheduledTraveltime.reset_index(inplace=True)
FMT = '%H:%M:%S'

for r in range(len(sheduledTraveltime)):

    sheduledTraveltime.loc[r,
                           'date'] = str(sheduledTraveltime.loc[r, 'arrivalTime_x'])[:10]
    sheduledTraveltime.loc[r,
                           'departure'] = str(sheduledTraveltime.loc[r, 'arrivalTime_x'])[11:19]
    sheduledTraveltime.loc[r,
                           'arrival'] = str(sheduledTraveltime.loc[r, 'arrivalTime_y'])[11:19]

    sheduledTraveltime.loc[r, 'scheduledTravelTime'] = (datetime.strptime(
        sheduledTraveltime.loc[r, 'arrival'], FMT) - datetime.strptime(sheduledTraveltime.loc[r, 'departure'], FMT)).total_seconds()/60
sheduledTraveltime = sheduledTraveltime[[
    'routeID', 'fromStop', 'toStop', 'date', 'departure', 'arrival', 'scheduledTravelTime']]
sheduledTraveltime.drop_duplicates(inplace=True)
print(sheduledTraveltime)

sheduledTraveltime.to_csv(
    'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/sheduledTraveltime.csv', index=False)

# # input from the user
# main_from_date = '21.07.2019'
# main_to_date = '22.07.2019'
# from_time = '16:00:00'
# to_time = '20:00:00'


# # retrieive actual travel times
# stops = [(x, y) for x, y in zip(crRoutes['firstStop'], crRoutes['lastStop'])]
# actualTravelTime = pd.DataFrame(
#     columns=['routeID', 'fromStop', 'toStop', 'departure', 'arrival', 'actualTravelTimeMin'])

# for stop in stops:

#     from_stop = stop[0]
#     to_stop = stop[1]
#     print("Retreiving data from", from_stop, "to", to_stop)
#     actualTravelTime = actualTravelTime.append(get_actual_travel_times(
#         main_from_date, main_to_date, from_time, to_time, from_stop, to_stop))


# ids = actualTravelTime.routeID.unique()
# t = actualTravelTime[['routeID', 'actualTravelTimeMin']]
# t.index.name = 'my_index'
# table = pd.pivot_table(t, index='my_index', columns='routeID',
#                        values="actualTravelTimeMin")
# table.to_csv(
#     'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/traveltime_test.csv', index=False)

# print(actualTravelTime)

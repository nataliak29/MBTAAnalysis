from get_route_ids import get_route_ids
from get_actual_travel_times import get_actual_travel_times
from get_representative_trip import get_representative_trip
import pandas as pd


routes = get_route_ids()
crRoutes = routes[routes.iloc[:, 1] == "Commuter Rail"]
print(crRoutes)


# input from the user
main_from_date = '14.07.2019'
main_to_date = '15.07.2019'
from_time = '16:00:00'
to_time = '20:00:00'


# retrieive actual travel times
stops = [(x, y) for x, y in zip(crRoutes['firstStop'], crRoutes['lastStop'])]
actualTravelTime = pd.DataFrame(
    columns=['routeID', 'fromStop', 'toStop', 'departure', 'arrival', 'travelTimeMin'])

for stop in stops:

    from_stop = stop[1]
    to_stop = stop[0]
    print("Retreiving data from", from_stop, "to", to_stop)
    actualTravelTime = actualTravelTime.append(get_actual_travel_times(
        main_from_date, main_to_date, from_time, to_time, from_stop, to_stop))


# ids = actualTravelTime.routeID.unique()
# t = actualTravelTime[['routeID', 'travelTimeMin']]
# t.index.name = 'my_index'
# table = pd.pivot_table(t, index='my_index', columns='routeID',
#                        values="travelTimeMin")
# table.to_csv(
#     'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/traveltime_test.csv', index=False)

print(actualTravelTime)

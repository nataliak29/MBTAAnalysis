from get_routes_names import get_routes_names
from get_travel_times import get_travel_times

import pandas as pd



main_from_date='1.01.2019'
main_to_date = '1.07.2019'
from_time='16:00:00'
to_time='20:00:00'

routes=get_routes_names()
cr=routes[routes.iloc[:,2]=="Commuter Rail"]

stops = [(x,y) for x,y in zip(cr['firstStop'],cr['lastStop'])]
traveltime= pd.DataFrame(columns=['routeID','fromStop','toStop','departure','arrival','travelTimeMin'])

for stop in stops:

    from_stop=stop[1]
    to_stop=stop[0]
    print("Retreiving data from",from_stop,"to",to_stop)
    traveltime=traveltime.append(get_travel_times(main_from_date,main_to_date,from_time,to_time,from_stop,to_stop))




ids=traveltime.routeID.unique()
t=traveltime[['routeID','travelTimeMin']]
t.index.name = 'foo'
# t.reset_index(inplace=True)


table =pd.pivot_table(t, index ='foo',columns= 'routeID', values="travelTimeMin")
table.to_csv('commuteRail/traveltime.csv')
# t.pivot( index='foo', columns ='routeID', values =['travelTimeMin'])
print(table)

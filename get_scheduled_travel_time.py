from get_route_ids import get_route_ids
from get_route_schedule import get_route_schedule
import pandas as pd
from datetime import datetime, timedelta, date


main_from_date = '2019-07-22'
main_to_date = '2019-07-24'
from_time = '06:00'
to_time = '22:00'
routeID = 'CR-Fairmount'
directionID = 0


def get_scheduled_travel_time(routeID, main_from_date, main_to_date, from_time, to_time, directionID):
    schedule = pd.DataFrame(
        columns=['routeID',
                 'tripID',
                 'date',
                 'stopID',
                 'stopSequence',
                 'arrivalTime',
                 'departureTime'])
    print('Retreiving schedules for routes...')

    numberOfDays = int((datetime.strptime(main_to_date, "%Y-%m-%d") -
                        datetime.strptime(main_from_date, "%Y-%m-%d")).days)
    print('Retreiving scheduled travel time data for', numberOfDays, 'days...')

    for date_date in (datetime.strptime(main_from_date, "%Y-%m-%d") + timedelta(n) for n in range(numberOfDays)):
        date = str(date_date)[:10]
        schedule = schedule.append(get_route_schedule(
            routeID, date, directionID, from_time, to_time))

    schedule['lastStop'] = schedule.groupby(['routeID', 'tripID', 'date'])[
        'stopSequence'].transform(max)
    schedule['firstStop'] = schedule.groupby(['routeID', 'tripID', 'date'])[
        'stopSequence'].transform(min)
    schedule = schedule[(schedule['stopSequence'] == schedule['lastStop']) | (
        schedule['stopSequence'] == schedule['firstStop'])]

    sheduledTraveltime = schedule.merge(
        right=schedule, left_on=['routeID', 'tripID', 'date'], right_on=['routeID', 'tripID', 'date'])

    sheduledTraveltime = sheduledTraveltime[sheduledTraveltime.stopSequence_x <
                                            sheduledTraveltime.stopSequence_y]
    sheduledTraveltime = sheduledTraveltime[[
        'routeID', 'date', 'tripID', 'stopID_x', 'arrivalTime_x', 'stopID_y', 'arrivalTime_y']]
    sheduledTraveltime = sheduledTraveltime.rename(
        columns={'stopID_x': 'fromStop', 'stopID_y': 'toStop'})
    sheduledTraveltime = sheduledTraveltime.reindex(
        columns=['routeID', 'date', 'tripID', 'fromStop', 'toStop', 'arrivalTime_x', 'arrivalTime_y'])

    sheduledTraveltime.reset_index(inplace=True)

    for r in range(len(sheduledTraveltime)):

        sheduledTraveltime.loc[r,
                               'departure'] = str(sheduledTraveltime.loc[r, 'arrivalTime_x'])[11:19]
        sheduledTraveltime.loc[r,
                               'arrival'] = str(sheduledTraveltime.loc[r, 'arrivalTime_y'])[11:19]

        sheduledTraveltime.loc[r, 'scheduledTravelTime'] = (datetime.strptime(
            sheduledTraveltime.loc[r, 'arrival'], '%H:%M:%S') - datetime.strptime(sheduledTraveltime.loc[r, 'departure'], '%H:%M:%S')).total_seconds()/60

    sheduledTraveltime = sheduledTraveltime[[
        'routeID', 'tripID', 'date', 'fromStop', 'toStop', 'departure', 'arrival', 'scheduledTravelTime']]
    sheduledTraveltime.drop_duplicates(inplace=True)

    return sheduledTraveltime


# print(get_scheduled_travel_time(routeID, main_from_date,
#                                 main_to_date, from_time, to_time, directionID))

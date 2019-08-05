import pandas as pd
from datetime import datetime, timedelta, date
import time
import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar


def clean_travel_times():
    # prepare calendar to look up holidays
    dr = pd.date_range(start='2017-01-01', end='2019-09-01')
    cal = calendar()
    holidays = cal.holidays(start=dr.min(), end=dr.max())
    #import data
    data = pd.read_csv(
        'actualTravelTime.csv')
    ####Clean data####

    # we want to consentraite the attention only on trains that are coming from the city to surubs (from North or South Stations)
    data = data[(data.loc[:, 'fromStop'] == 'South Station') |
                (data.loc[:, 'fromStop'] == 'North Station')]
    # find the furthest stop on the route
    data['furthestStopBenchmark'] = data.groupby(['routeID',
                                                  'date', 'fromStop', 'departure'])['benchmarkTravelTime'].transform(max)
    data = data[data['furthestStopBenchmark'] == data['benchmarkTravelTime']]

    ###Feature generation####

    # create route id dummy
    route_dummy = pd.get_dummies(data['routeID'])
    data = pd.concat([data, route_dummy], axis=1)

    # create fromStop dummy
    fromStop_dummy = pd.get_dummies(data['fromStop'])
    data = pd.concat([data, fromStop_dummy], axis=1)

    # create day of the week, departure hour, month, time of the day (morning, evening),weekend,rush hour features
    data['departure_time'] = pd.to_datetime(
        data['date'] + ' ' + data['departure'])

    data['weekday'] = data['departure_time'].dt.dayofweek
    data['hour'] = data['departure_time'].dt.hour
    data['month'] = data['departure_time'].dt.month

    # morning is considered to be between 5 am and 12pm
    data['morning'] = np.where((data['hour'] < 12) & (data['hour'] > 5), 1, 0)

    # evening is considered to be between 4 pm and 11 pm
    data['evening'] = np.where((data['hour'] > 16) & (data['hour'] < 23), 1, 0)
    data['weekend'] = np.where((data['weekday'] == 5) |
                               (data['weekday'] == 6), 1, 0)

    # rush hour is considered to be between 7 am and 10 am; 4 pm and 8 pm
    data['rush_hour'] = np.where(((data['hour'] > 7) & (data['hour'] < 10)) |
                                 ((data['hour'] > 16) & (data['hour'] < 20)), 1, 0)

    # create a boolean flag is data is a holiday
    data['is_holiday'] = data['departure_time'].dt.date.astype(
        'datetime64').isin(holidays)
    data['holiday'] = np.where((data['is_holiday'] == True), 1, 0)

    # the delay label is determined to be 1 if actual travel time is above scheduled (benchmark) travel time --delay
    # the delay label is determined to be 0 if actual travel time is below scheduled (benchmark) travel time --no delay
    data['delay_label'] = np.where((data['delay'] > 0), 1, 0)

    # remove unnecessary columns from the resulting table
    data = data.drop(['departure_time', 'is_holiday', 'furthestStopBenchmark',
                      'routeID', 'date', 'fromStop', 'toStop', 'departure', 'arrival'], axis=1)

    data.to_csv(
        'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/data2.csv', index=False)
    return data

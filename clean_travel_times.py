import pandas as pd

data = pd.read_csv(
    'actualTravelTime.csv')

print(data)
# we want to consentraite the attention only on trains that are coming from the city to surubs (from North or South Stations)
data = data[(data.loc[:, 'fromStop'] == 'South Station') |
            (data.loc[:, 'fromStop'] == 'North Station')]

data['furthestStopBenchmark'] = data.groupby(['routeID',
                                              'date', 'fromStop', 'departure'])['benchmarkTravelTime'].transform(max)
data = data[data['furthestStopBenchmark'] == data['benchmarkTravelTime']]
# data = data[(data.loc[:, 'furthestStopBenchmark'] == data.loc[:, 'benchmarkTravelTime'] ]
print(data)
data.to_csv(
    'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/data2.csv', index=False)

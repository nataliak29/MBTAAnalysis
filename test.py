import pandas as pd
data = pd.read_csv(
    'https://gist.githubusercontent.com/chrtze/c74efb46cadb6a908bbbf5227934bfea/raw/c32d94689dd432609c55d1758d8e69c59f94f802/traffic_weekly.csv')

data.to_csv(
    'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/data.csv', index=False)

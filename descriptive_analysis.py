from clean_travel_times import clean_travel_times
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = clean_travel_times()
print(data)
x = data.loc[:, 'delay']
plt.hist(x, bins=20)
plt.ylabel('No of times')
plt.show()

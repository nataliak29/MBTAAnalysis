from matplotlib.legend_handler import HandlerLine2D
from clean_travel_times import clean_travel_times
from sklearn.model_selection import train_test_split
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
import matplotlib as mpl
import matplotlib.pyplot as plt

data = clean_travel_times()
print(data)
data = data.drop(['actualTravelTimeMin', 'delay'], axis=1)
print(data)
yVar = data.loc[:, 'delay_label']
print(yVar)
xVar = data.drop(['delay_label'], axis=1)
x_train, x_test, y_train, y_test = train_test_split(xVar, yVar, test_size=0.2)
clf = RandomForestClassifier(
    n_estimators=75, max_depth=18)

clf.fit(x_train, y_train)

preds = clf.predict(x_test)
print(pd.crosstab(y_test, preds, rownames=[
      'Actual Result'], colnames=['Predicted Result']))
print(list(zip(x_train, clf.feature_importances_)))
data.to_csv(
    'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/data3.csv', index=False)
false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, preds)
roc_auc = auc(false_positive_rate, true_positive_rate)
print(roc_auc)

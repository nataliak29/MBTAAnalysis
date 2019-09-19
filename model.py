from clean_travel_times import clean_travel_times
from sklearn.model_selection import train_test_split
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

data = clean_travel_times()
print(data)
data = data.drop(['actualTravelTimeMin', 'delay'], axis=1)
print(data)
yVar = data.loc[:, 'delay_label']
print(yVar)
xVar = data.drop(['delay_label'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(xVar, yVar, test_size=0.2)
clf = RandomForestClassifier(n_jobs=2, random_state=0)

clf.fit(X_train, y_train)
RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                       max_depth=None, max_features='auto', max_leaf_nodes=None,
                       min_impurity_split=1e-07, min_samples_leaf=1,
                       min_samples_split=2, min_weight_fraction_leaf=0.0,
                       n_estimators=10, n_jobs=2, oob_score=False, random_state=0,
                       verbose=0, warm_start=False)
preds = clf.predict(X_test)
print(pd.crosstab(y_test, preds, rownames=[
      'Actual Result'], colnames=['Predicted Result']))
print(list(zip(X_train, clf.feature_importances_)))
data.to_csv(
    'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/data3.csv', index=False)

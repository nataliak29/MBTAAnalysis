from matplotlib.legend_handler import HandlerLine2D
from clean_travel_times import clean_travel_times
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
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
clf = RandomForestClassifier()

clf.fit(x_train, y_train)

preds = clf.predict(x_test)
# print(pd.crosstab(y_test, preds, rownames=[
#       'Actual Result'], colnames=['Predicted Result']))
# print(list(zip(x_train, clf.feature_importances_)))
# data.to_csv(
#     'C:/Users/nkukushkina/Documents/GitHub/MBTAAnalysis/data3.csv', index=False)
false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, preds)
roc_auc = auc(false_positive_rate, true_positive_rate)
print(roc_auc)

# n_estimators = [1, 2, 4, 8, 16, 32, 64, 100, 200]
# train_results = []
# test_results = []
# for estimator in n_estimators:
#     rf = RandomForestClassifier(n_estimators=estimator, n_jobs=-1)
#     rf.fit(x_train, y_train)
#     train_pred = rf.predict(x_train)
#     false_positive_rate, true_positive_rate, thresholds = roc_curve(
#         y_train, train_pred)
#     roc_auc = auc(false_positive_rate, true_positive_rate)
#     train_results.append(roc_auc)
#     y_pred = rf.predict(x_test)
#     false_positive_rate, true_positive_rate, thresholds = roc_curve(
#         y_test, y_pred)
#     roc_auc = auc(false_positive_rate, true_positive_rate)
#     test_results.append(roc_auc)
# line1, = plt.plot(n_estimators, train_results, 'b', label='Train AUC')
# line2, = plt.plot(n_estimators, test_results, 'r', label='Test AUC')
# plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
# plt.ylabel('AUC score')
# plt.xlabel('n_estimators')
# plt.show()


# max_depths = np.linspace(1, 32, 32, endpoint=True)
# train_results = []
# test_results = []
# for max_depth in max_depths:
#     rf = RandomForestClassifier(max_depth=max_depth, n_jobs=-1)
#     rf.fit(x_train, y_train)
#     train_pred = rf.predict(x_train)
#     false_positive_rate, true_positive_rate, thresholds = roc_curve(
#         y_train, train_pred)
#     roc_auc = auc(false_positive_rate, true_positive_rate)
#     train_results.append(roc_auc)
#     y_pred = rf.predict(x_test)
#     false_positive_rate, true_positive_rate, thresholds = roc_curve(
#         y_test, y_pred)
#     roc_auc = auc(false_positive_rate, true_positive_rate)
#     test_results.append(roc_auc)
# line1, = plt.plot(max_depths, train_results, 'b', label='Train AUC')
# line2, = plt.plot(max_depths, test_results, 'r', label='Test AUC')
# plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
# plt.ylabel('AUC score')
# plt.xlabel('Tree depth')
# plt.show()


# min_samples_splits = np.linspace(0.1, 1.0, 10, endpoint=True)
# train_results = []
# test_results = []
# for min_samples_split in min_samples_splits:
#     rf = RandomForestClassifier(min_samples_split=min_samples_split)
#     rf.fit(x_train, y_train)
#     train_pred = rf.predict(x_train)
#     false_positive_rate, true_positive_rate, thresholds = roc_curve(
#         y_train, train_pred)
#     roc_auc = auc(false_positive_rate, true_positive_rate)
#     train_results.append(roc_auc)
#     y_pred = rf.predict(x_test)
#     false_positive_rate, true_positive_rate, thresholds = roc_curve(
#         y_test, y_pred)
#     roc_auc = auc(false_positive_rate, true_positive_rate)
#     test_results.append(roc_auc)
# line1, = plt.plot(min_samples_splits, train_results, 'b', label='Train AUC')
# line2, = plt.plot(min_samples_splits, test_results, 'r', label='Test AUC')
# plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
# plt.ylabel('AUC score')
# plt.xlabel('min samples split')
# plt.show()


# min_samples_leafs = np.linspace(0.1, 0.5, 5, endpoint=True)
# train_results = []
# test_results = []
# for min_samples_leaf in min_samples_leafs:
#     rf = RandomForestClassifier(min_samples_leaf=min_samples_leaf)
#     rf.fit(x_train, y_train)
#     train_pred = rf.predict(x_train)
#     false_positive_rate, true_positive_rate, thresholds = roc_curve(
#         y_train, train_pred)
#     roc_auc = auc(false_positive_rate, true_positive_rate)
#     train_results.append(roc_auc)
#     y_pred = rf.predict(x_test)
#     false_positive_rate, true_positive_rate, thresholds = roc_curve(
#         y_test, y_pred)
#     roc_auc = auc(false_positive_rate, true_positive_rate)
#     test_results.append(roc_auc)
# line1, = plt.plot(min_samples_leafs, train_results, 'b', label='Train AUC')
# line2, = plt.plot(min_samples_leafs, test_results, 'r', label='Test AUC')
# plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
# plt.ylabel('AUC score')
# plt.xlabel('min samples leaf')
# plt.show()


max_features = list(range(1, xVar.shape[1]))
train_results = []
test_results = []
for max_feature in max_features:
    rf = RandomForestClassifier(max_features=max_feature)
    rf.fit(x_train, y_train)
    train_pred = rf.predict(x_train)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(
        y_train, train_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)
    y_pred = rf.predict(x_test)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(
        y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)
line1, = plt.plot(max_features, train_results, 'b', label='Train AUC')
line2, = plt.plot(max_features, test_results, 'r', label='Test AUC')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('max features')
plt.show()

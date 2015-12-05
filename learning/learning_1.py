import csv

import numpy as np
import pandas as pd
from sklearn import svm, neighbors, tree, dummy
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, mean_absolute_error, \
    mean_squared_error, median_absolute_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from learning.features_1 import features

file_name = "results_without_ctrls_with_scale.csv"

data_dir = '../data/MovieVector4/1_yoni/'
data_file = data_dir + 'data_raw.csv'

PREDICTABLE = ['rating', 'success', 'category']

data = pd.io.parsers.read_csv(data_file)
N_SAMPLES = len(data)
TEST_SIZE = 0.2

# Test on NEW movies !
train, test = data.head(int(N_SAMPLES * (1 - TEST_SIZE))), data.tail(
    int(N_SAMPLES * TEST_SIZE))

print "len : %s " %len(train)
print "train set rating variance : %s" %np.var(test['rating'])

estimators = [
    ("Dummy", dummy.DummyRegressor()),
    ("SVR_linear", svm.SVR(kernel='linear', cache_size=1000)),
    ("SVR_rbf", svm.SVR(kernel='rbf', cache_size=1000)),
    ("KNN", KNeighborsRegressor()),
    ("Random Forest", RandomForestRegressor())
]

metrics = [
    ("mean_absolute_error", mean_absolute_error),
    ("mean_squared_error", mean_squared_error),
    ("median_absolute_error", median_absolute_error),
    ("r2_score", r2_score)
]

with open(data_dir + file_name, 'wb') as fp:
    writer = csv.writer(fp)
    writer.writerow(['estimator'] + [x[0] for x in metrics])

for estimator_name, estimator in estimators:
    pipeline = Pipeline([
        ('feature_extractor', features),
        ('estimator', estimator)
    ])
    pipeline.fit(train, train['rating'])
    with open(data_dir + "/tmp_%s.csv" % estimator_name, 'wb', 0) as fp:
        writer = csv.writer(fp)
        writer.writerow(['true', 'predicted','diff'])
        pred = pipeline.predict(test)
        tru = test['rating']
        for pr, tr in zip(pred, tru):
            writer.writerow([tr, pr,abs(pr-tr)])

    """
    with open(data_dir + file_name, 'ab') as fp:
        writer = csv.writer(fp)
        pred = pipeline.predict(test)
        true_res = test['rating']
        row = [estimator_name] + [met[1](pred, true_res) for met in metrics]
        writer.writerow(row)
    """

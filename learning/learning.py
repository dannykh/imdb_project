from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, mean_absolute_error, \
    mean_squared_error, median_absolute_error, r2_score
from prep.features_1 import features
from sklearn import svm, neighbors, tree, dummy
from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler, StandardScaler

file_name = "results_with_normalization_scaling_guess1.csv"

data_dir = '../data/MovieVector4/9_dan_full/'
data_file = data_dir + 'data_raw.csv'

PREDICTABLE = ['rating', 'success', 'category']

data = pd.io.parsers.read_csv(data_file)
N_SAMPLES = len(data)
TEST_SIZE = 0.2

# Test on NEW movies !
train, test = data.head(int(N_SAMPLES * (1 - TEST_SIZE))), data.tail(
    int(N_SAMPLES * TEST_SIZE))

print len(train)

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

from sklearn.preprocessing import Imputer

for estimator_name, estimator in estimators:
    pipeline = Pipeline([
        ('feature_extractor', features),
        ('Imputer', Imputer()),
        ('normalization', StandardScaler()),
        ('scaling', MinMaxScaler((-1, 1))),
        ('estimator', estimator)
    ])
    pipeline.fit(train, train['rating'])
    print "%s %s "%estimator_name%estimator.coef_
    with open(data_dir + "/tmp_%s.csv" % estimator_name, 'wb', 0) as fp:
        writer = csv.writer(fp)
        writer.writerow(['true','predicted'])
        pred=pipeline.predict(test)
        tru=test['rating']
        for pr,tr in zip(pred,tru):
            writer.writerow([tr,pr])

    """
    with open(data_dir + file_name, 'ab') as fp:
        writer = csv.writer(fp)
        pred = pipeline.predict(test)
        true_res = test['rating']
        row = [estimator_name] + [met[1](pred, true_res) for met in metrics]
        writer.writerow(row)
    """
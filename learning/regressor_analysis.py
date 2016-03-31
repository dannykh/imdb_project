"""
This module handles the analysis and comparison of regressors used in the project.
Each regressor is trained and tested on vectors processed in preprocessing module.

Settings should be set to run the test.
Output will be in data/analysis/run_id (relevant run_id will probably be the biggest/last).
"""
import pandas as pd
import numpy as np
import pandas as pd
from sklearn import svm, neighbors, tree, dummy, linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, mean_absolute_error, \
    mean_squared_error, median_absolute_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from data import meta
import csv
# SETTINGS ------------------------------------------------

from preprocessing import features

# If set to True, a csv with actual rating vs prediction will be generated as well.
RAW_RATING_OUTPUT = False

# Base dir, to which all names in data_files are relative.
base_d = "../"

# Files from which to draw feature vectors. The vectors are concatenated in the order
# they appear in the list. It is IMPORTANT that rating.csv is the first file on the list.
data_files = [
    'data/MovieVector4/Parts/rating.csv',
    #'data/MovieVector4/Parts/basic_data.csv',
    #'data/MovieVector4/Parts/bin_data.csv',
    #'data/MovieVector4/Parts/reg_avg.csv'#,
    #'data/MovieVector4/Parts/y_avg.csv',
    'data/MovieVector4/Parts/y_v_avg.csv'
]

# Portion of movies to be taken as test set for model evaluation.
# Consequently, training set will be of size (1-TEST_SIZE)*(num of movies in db)
TEST_SIZE = 0.2

# List of estimators to be examined
estimators = [
    ("Dummy", dummy.DummyRegressor()),
    ("Least Squares", linear_model.LinearRegression()),
    ("SVR_linear", svm.SVR(kernel='linear', cache_size=1000)),
    ("SVR_rbf", svm.SVR(kernel='rbf', cache_size=1000)),
    ("KNN", KNeighborsRegressor()),
    ("Random Forest", RandomForestRegressor())
]

# Metrics by which to examine the estimators.
metrics = [
    ("mean_absolute_error", mean_absolute_error),
    ("mean_squared_error", mean_squared_error),
    ("median_absolute_error", median_absolute_error),
    ("r2_score", r2_score)
]

# END SETTINGS ----------------------------------------------

data_files = map(lambda x: base_d + x, data_files)

if len(data_files) > 1:
    data = reduce(lambda left, right: pd.merge(left, right, on='id'),
            (pd.read_csv(data_file) for data_file in data_files))
else:
    data = pd.read_csv(data_files[0])

N_SAMPLES = len(data)
train, test = data.head(int(N_SAMPLES * (1 - TEST_SIZE))), data.tail(
        int(N_SAMPLES * TEST_SIZE))

train_stats = [
    ('variance', np.var(test['rating']))
]

data_dir = meta.DataDirControl('results')
data_path = data_dir.create_version()

with open(data_dir.get_file("about.txt"), 'wb') as fp:
    fp.write("Vector files : \n")
    for fname in data_files:
        fp.write("- %s\n" % fname)

    fp.write("\nTrain set size = %s \n" % (1 - TEST_SIZE))

    fp.write("\nTraining set stats : \n")
    for stat, val in train_stats:
        fp.write("- %s : %s \n" % (stat, val))

    fp.write("\n Estimators : \n")
    for est in estimators:
        fp.write("- %s %s \n" % (est[0], est[1].get_params()))

    fp.write("\n Metrics : \n")
    for met in metrics:
        fp.write("- %s \n" % met[0])

results = {}

for estimator_name, estimator in estimators:
    pipeline = Pipeline([
        ('feature_extractor', features),
        ('estimator', estimator)
    ])
    pipeline.fit(train, train['rating'])

    pred = pipeline.predict(test)
    true_res = test['rating']

    if RAW_RATING_OUTPUT:
        pd.DataFrame({
            "True": true_res,
            "Predicted": pred,
            "Diff": [abs(x - y) for x, y in zip(true_res, pred)]
        }).to_csv(data_dir.get_file('%s_raw.csv' % estimator_name))

    results.update({estimator_name: [met[1](pred, true_res) for met in metrics]})

df = pd.DataFrame(results, [met[0] for met in metrics])
df.to_csv(data_dir.get_file('results.csv'))
# df.to_csv(data_dir.get_file('results.txt'), "|")

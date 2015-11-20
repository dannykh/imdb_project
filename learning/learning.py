from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from prep.features_1 import features
import pandas as pd

data_file = 'data/MovieVector3/2/data_raw.csv'

PREDICTABLE = ['score', 'success', 'category']

data = pd.io.parsers.read_csv(data_file)
N_SAMPLES = len(data)
TEST_SIZE = 0.8

# Test on NEW movies !
train, test = data.head(N_SAMPLES * (1 - TEST_SIZE)), data.head(
    N_SAMPLES * TEST_SIZE)


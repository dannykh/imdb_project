"""
All should be in form of a pipeline starting with a class implementing fit,
and transform.
fit() does nothing (returns self )
transform : receives a list of movies and returns and returns a list of
processed vectors, featurizing the movies. Order between movies should be kept
"""

from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.preprocessing import OneHotEncoder, Imputer, StandardScaler,MinMaxScaler
from sklearn.feature_extraction import DictVectorizer
import numpy as np
import pandas as pd


class InfoExtractor(TransformerMixin, BaseEstimator):
    """
    Extract info from Movies in form of a mapping : info_name->info
    """

    def __init__(self, info):
        self.info = info

    def fit(self, *_):
        return self

    def transform(self, data):
        return [x[self.info] for x in data]


class GenreTransformer(TransformerMixin, BaseEstimator):
    def fit(self, *_):
        return self

    def transform(self, data):
        return [{"genre_%s" % tt: True for tt in x} for x in data]


class ScaleBinary(TransformerMixin, BaseEstimator):
    def __init__(self, range):
        self.range = range

    def fit(self, *_):
        return self

    def transform(self, data):
        return [map(lambda x: self.range[int(x)], rw) for rw in data]


genre_featurizer = Pipeline([
    ('info_extractor', InfoExtractor('genres')),
    ('genre_transform', GenreTransformer()),
    ('dict_vectorizer', DictVectorizer())
    # ('scale', ScaleBinary((-1, 1)))
])


class Averages(TransformerMixin, BaseEstimator):
    def fit(self, *_):
        return self

    def transform(self, data):
        return data.iloc[:, 1:]


class AddControl(TransformerMixin, BaseEstimator):
    def fit(self, *_):
        return self

    def transform(self, data):
        def binarizer(val):
            return -1 if pd.isnull(val) else 1

        controls_funcs = [
            ('director_nan', 'director avg rating')
        ]

        controls = {}
        for ctrl_nm, ctrl_col in controls_funcs:
            controls.update({ctrl_nm: [binarizer(x) for x in data[ctrl_col]]})

        return pd.DataFrame(controls)


avgs = Pipeline([
    ('avg_get', Averages()),
    ('Imputer', Imputer()),
    ('normalization', StandardScaler()),
    ('scaling',MinMaxScaler((-1,1)))
])

features = FeatureUnion([
    ('avgs_simple', avgs)
    #('controls', AddControl())
])



if __name__ == "__main__":
    from prep.IMDB import IMDB

    data_dir = '../data/MovieVector4/1_yoni/'
    data_file = data_dir + 'data_raw.csv'
    data = pd.io.parsers.read_csv(data_file)

    res = pd.DataFrame(features.fit_transform(data))

    res.to_csv(data_dir + 'with_controls.csv')

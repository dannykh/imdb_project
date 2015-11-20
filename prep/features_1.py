"""
All should be in form of a pipeline starting with a class implementing fit,
and transform.
fit() does nothing (returns self )
transform : receives a list of movies and returns and returns a list of
processed vectors, featurizing the movies. Order between movies should be kept
"""

from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction import DictVectorizer
import numpy as np

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


# class QueryMap(TransformerMixin, BaseEstimator):



genre_featurizer = Pipeline([
    ('info_extractor', InfoExtractor('genres')),
    ('genre_transform', GenreTransformer()),
    ('dict_vectorizer', DictVectorizer())
    #('scale', ScaleBinary((-1, 1)))
])

features = FeatureUnion([
    ("title", make_pipeline(InfoExtractor('title'))),
    ("rating", make_pipeline(InfoExtractor('rating')))
    #("genres", genre_featurizer)
])


def just_transforms(feat, X):
    """Applies all transforms to the data, without applying last
       estimator.

    Parameters
    ----------
    X : iterable
        Data to predict on. Must fulfill input requirements of first step of
        the pipeline.
    """
    Xt = X
    for name, transform in feat.steps:
        Xt = transform.fit_transform(Xt)
    return Xt


if __name__ == "__main__":
    from IMDB import IMDB

    conn = IMDB()
    movies = []
    for mov in conn.get_all_movies(limit=3):
        try:
            mov.update()
            movies += [mov]
        except Exception, e:
            pass

    print features.fit_transform(movies)

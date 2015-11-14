from Model import Model
import numpy as np
from sklearn import svm, preprocessing, cross_validation
from sklearn.pipeline import make_pipeline


class SVM(Model):
    def __init__(self, feat_range=(-1, 1)):
        super(SVM, self).__init__()
        self.pipeline_form = (preprocessing.MinMaxScaler(feat_range), svm.SVR())
        self.pipeline = make_pipeline(*self.pipeline_form)
        self.classifier = make_pipeline(*self.pipeline_form)

    def evaluate(self, eval_methods=None):
        pass

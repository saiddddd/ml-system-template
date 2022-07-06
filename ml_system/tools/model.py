

from abc import ABC, abstractmethod
from sklearn.ensemble import RandomForestClassifier

import xgboost as xgb

from river import ensemble
from river.tree import HoeffdingAdaptiveTreeClassifier

import numpy as np
from tqdm import tqdm

import time


class Model(ABC):

    def __init__(self):
        self.__model = None

    def __init_model(self):
        raise NotImplementedError

    def fit(self, x, y):
        raise NotImplementedError

    def predict(self, x, pred_proba_cut_point):
        raise NotImplementedError

    def predict_proba(self, x):
        raise NotImplementedError


class SklearnRandonForest(Model, ABC):

    def __init__(self, *args, **kwargs):
        super(SklearnRandonForest).__init__()
        self.__init__model(*args, **kwargs)

    def __init__model(self, *args, **kwargs):

        self.__model = RandomForestClassifier(*args, **kwargs)

    def fit(self, x, y):
        print("going to train model")
        self.__model.fit(x, y)

    def predict(self, x, pred_proba_cut_point=0.5):
        return self.__model.predict(x)

    def predict_proba(self, x):
        return self.__model.predict_proba()


class XGBoostClassifier(Model, ABC):

    def __init__(self, *args, **kwargs):
        super(XGBoostClassifier).__init__()
        self.__init__model(*args, **kwargs)

    def __init__model(self, *args, **kwargs):

        self.__model = xgb.XGBClassifier(*args, **kwargs)

    def fit(self, x, y):
        print("go to train XGBoost Classifier")
        self.__model.fit(x, y)

    def predict(self, x, pred_proba_cut_point=0.5):
        print("using xgboost to predict result")
        prediction_result = self.__model.predict(x)
        return prediction_result

    def predict_proba(self, x):
        return self.__model.predict_proba()


class RFAdaptiveHoeffdingClassifier(Model, ABC):

    def __init__(self, *args, **kwargs):
        super(RFAdaptiveHoeffdingClassifier).__init__()
        self.__init__model(*args, **kwargs)

    def __init__model(self, *args, **kwargs):

        self.__model = ensemble.AdaBoostClassifier(
            model=HoeffdingAdaptiveTreeClassifier(
                *args, **kwargs
            ),
            n_models=20,
            seed=42
        )

    def fit(self, x, y):

        print('using hoeffding tree classifier to fit data')

        for index, row in tqdm(x.iterrows(), total=x.shape[0]):
            self.__model.learn_one(row, y[index])

        print("finish to train model")

    def predict(self, x, pred_proba_cut_point=0.5):

        pred_result_list = []
        for index, row in tqdm(x.iterrows(), total=x.shape[0]):
            try:
                pred_proba_result = self.__model.predict_proba_one(row)
                if isinstance(pred_proba_result, dict):
                    pred_proba_true = pred_proba_result.get(1)

                    if pred_proba_true > pred_proba_cut_point:
                        pred_result_list.append(1)
                    else:
                        pred_result_list.append(0)
            except:
                print("Unexpected error happen when do model prediction")
                time.sleep(1)

        return pred_result_list


    def predict_proba(self, x):

        pred_proba_result_list = []
        for index, row in tqdm(x.iterrows(), total=x.shape[0]):
            try:
                pred_proba_result = self.__model.predict_proba_one(row)
                if isinstance(pred_proba_result, dict):
                    pred_proba_true = pred_proba_result.get(1)
                    pred_proba_result_list.append(pred_proba_true)
                else:
                    raise TypeError("The Hoeffding Tree model prediction return result is not in dictionary type!!")
            except:
                print("Can not do model prediction this iterate!")

        return pred_proba_result_list




#------------------------------------------------------------------------#
# Appending others new model which have been desired to use in ml system #
#------------------------------------------------------------------------#




from abc import ABC, abstractmethod
from sklearn.ensemble import RandomForestClassifier

import xgboost as xgb

# from river


class Model(ABC):

    def __init__(self):
        self.__model = None

    def __init_model(self):
        raise NotImplementedError

    def fit(self, x, y):
        raise NotImplementedError

    def predict(self, x):
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

    def predict(self, x):
        self.__model.predict(x)


class XGBoostClassifier:

    def __init__(self, *args, **kwargs):
        super(XGBoostClassifier).__init__()
        self.__init__model(*args, **kwargs)

    def __init__model(self, *args, **kwargs):

        self.__model = xgb.XGBClassifier(*args, **kwargs)

    def fit(self, x, y):
        print("go to train XGBoost Classifier")
        self.__model.fit(x, y)

    def predict(self, x):
        print("using xgboost to predict result")
        prediction_result = self.__model.predict(x)
        return prediction_result

# class RFAdaptiveHoeffdingClassifier:
#
#     def __init__(self, *args, **kwargs):
#         super(RFAdaptiveHoeffdingClassifier).__init__()
#         self.__init_model(*args, **kwargs)
#
#     def __init__model(self, *args, **kwargs):
#
#         self.__model =


#------------------------------------------------------------------------#
# Appending others new model which have been desired to use in ml system #
#------------------------------------------------------------------------#


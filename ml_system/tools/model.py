

from abc import ABC, abstractmethod
from sklearn.ensemble import RandomForestClassifier


class Model(ABC):

    def __init__(self):
        self.__model = None

    def __init_model(self):
        raise NotImplementedError

    def fit(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError


class SklearnRandonForest:

    def __init__(self):
        super(SklearnRandonForest).__init__()
        self.__init__model()

    def __init__model(self, *args, **kwargs):
        pass
        # TODO: initialization of sklearn random forest model, ingress input hyperparameter.
        self.__model = RandomForestClassifier(
            n_estimators=10,
        )

    def fit(self, x, y):
        self.__model.fit(x, y)

    def predict(self, x):
        self.__model.predict(x)


#------------------------------------------------------------------------#
# Appending others new model which have been desired to use in ml system #
#------------------------------------------------------------------------#


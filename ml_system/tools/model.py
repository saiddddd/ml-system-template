

from abc import ABC, abstractmethod

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

    def __init__model(self, *args, **kwargs):
        pass
        # TODO: initialization of sklearn random forest model, ingress input hyperparameter.
        # self.__model =


#------------------------------------------------------------------------#
# Appending others new model which have been desired to use in ml system #
#------------------------------------------------------------------------#




from abc import ABC, abstractmethod

class Model(ABC):

    def __init__(self):
        pass

    def __init_model(self):
        raise NotImplementedError

    def fit(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError


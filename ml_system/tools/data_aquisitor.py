
from abc import ABC, abstractmethod


class DataAcquisitor(ABC):

    def __init__(self):

        self.__data_acquisitor_status = None

    @property
    def acquisitor_status(self):
        return self.__data_acquisitor_status

    @acquisitor_status.setter
    def acquisitor_status(self, running_status):
        self.__data_acquisitor_status = running_status

    @acquisitor_status.getter
    def get_data_acquisitor_status(self):
        self.__data_acquisitor_status()


class KafkaDataAcquisitor(DataAcquisitor):

    def __init__(self, bootstrap_server: str, topic: str):

        super(KafkaDataAcquisitor).__init__()


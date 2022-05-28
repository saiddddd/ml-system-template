
import json
from abc import ABC, abstractmethod
from kafka import KafkaConsumer


class DataAcquisitor(ABC):

    """
    Data Acquisitor is responsible for access streaming data source,
    """

    def __init__(self, data_acq_name: str, data_source: str):
        """
        The abstraction of objects dealing with streaming data source extraction
        for explict data source will be implemented by following concrete class.
        :param data_acq_name: set the data acquisitor name, which will use by data acquisitor coordinator.
        :param data_source: set of the data source.
        """
        self.__data_acquisitor_status = None
        self.__data_acq_name = data_acq_name
        self._data_source = data_source

    def __str__(self):
        return self.__data_acq_name

    def __repr__(self):
        return self.__data_acq_name

    @property
    def data_acquisitor_status(self):
        return self.__data_acquisitor_status

    @data_acquisitor_status.setter
    def data_acquisitor_status(self, status):
        if status == 'running' or status == 'stop':
            self.__data_acquisitor_status = status
        else:
            print("Error of status setting {}. please using running or stop instead!".format(status))

    @data_acquisitor_status.getter
    def data_acquisitor_status(self):

        if self.__data_acquisitor_status is 'running' or self.__data_acquisitor_status is 'stop':
            return self.__data_acquisitor_status
        else:
            print(self.__data_acquisitor_status)
            raise Exception


    @abstractmethod
    def _data_acq_job(self):
        """
        core part of data acquisitor,
        implement of data acquisition lob and logic based on specific data source
        :return:
        """
        raise NotImplementedError

    def get_data_source(self):
        return self._data_source

    def run(self):
        """
        Executing Data Acquisition which implement in concrete class for satisfied data source requirements.

        Using data_acquisitor_status

        :return:
        """

        self.data_acquisitor_status = 'running'

        while self.data_acquisitor_status is 'running':
            self._data_acq_job()

        print("{} is stopped".format(__name__))

    def stop(self):
        self.data_acquisitor_status = 'stop'


class KafkaDataAcquisitor(DataAcquisitor):

    def __init__(self, data_acq_name: str, bootstrap_server: str, topic: str):
        """
        The concrete class to deal with kafka data source,
        plays the role of kafka consumer and pump the data in to ML System.
        :param data_acq_name:
        :param bootstrap_server:
        :param topic:
        """
        super(KafkaDataAcquisitor, self).__init__(data_acq_name=data_acq_name, data_source=bootstrap_server)
        self.__topic = topic

        self.__kafka_consumer = self._init_kafka_consumer()
        self.__kafka_fetch_data_mode = None

        # fetched data which is going to return
        self.__data = None

    '''design the property to distinguish kafka fetching data mode, is poll or iterate
    '''
    @property
    def kafka_fetch_data_mode(self):
        return self.__kafka_fetch_data_mode

    @kafka_fetch_data_mode.setter
    def kafka_fetch_data_mode(self, fetch_mode):
        if fetch_mode == 'poll' or fetch_mode == 'iterate':
            self.__kafka_fetch_data_mode = fetch_mode
        else:
            raise RuntimeError

    @kafka_fetch_data_mode.getter
    def kafka_fetch_data_mode(self):
        if self.__kafka_fetch_data_mode is not None:
            return self.__kafka_fetch_data_mode
        else:
            raise RuntimeError

    def _init_kafka_consumer(self):
        """
        initialization of kafka consumer
        :return:
        """

        kafka_consumer = KafkaConsumer(
            self.__topic,
            bootstrap_servers=[self._data_source],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        return kafka_consumer


    def _data_acq_job(self):
        pass

    def get_data(self):
        return self.__data








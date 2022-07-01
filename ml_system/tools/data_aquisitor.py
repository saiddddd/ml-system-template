
import threading
import json
import time
from abc import ABC, abstractmethod
from kafka import KafkaConsumer

import pandas as pd


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

        if self.__data_acquisitor_status == 'running' or self.__data_acquisitor_status == 'stop':
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
        Run method, Executing Data Acquisition which implement in concrete class for satisfied data source requirements.
        Using data_acquisitor_status

        procedure to start data acquisitor

        Examples
        --------

        >>> data_acq = DataAcquisitor()  # initialize data acquisitor by constructor
        >>> servicer = Thread(target=data_acq.run)  # put this run method to a Thread and execute by thread module
        >>> # this run method will assign `running` status to data acquisitor and make it process as function implemented
        >>> servicer.start()  # start the servicer thread

        --------
        :return:
        """

        self.data_acquisitor_status = 'running'

        print("Data acquisitor: {} is running".format(self.__data_acq_name))

        while self.data_acquisitor_status == 'running':
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
        self.__data = []

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
        """
        Implement of kafka data source acquisition core part.
        polling data from kafka message queue and set it onto
        :return:
        """

        # one polling from kafka broker,
        data_polling_result = self.__kafka_consumer.poll(
            timeout_ms=1000,
            max_records=None,
            update_offsets=True
        )
        for key, value in data_polling_result.items():
            # kafka polling result.items() will return one batch of polling data with key == topic.
            # if here only one topic going to consume, the for loop will iterate only one time.

            # appending fetched data from kafka to queue. Waiting to flush
            self.__data.extend(value)
        time.sleep(1)

    def get_data_fetcher(self) -> list:
        """
        Generator feature,
        for ML server side to fetch data by iterator.
        Terminated while process stop.
        :return:
        """

        while self.data_acquisitor_status == 'running':
            time.sleep(1)

            if len(self.__data) > 0:
                fetched_data = self.__data
                self.__data = []

                # convert kafka poll data into pandas dataframe
                # 2d list
                accumulated_data = []
                for record in fetched_data:
                    row_data = record.value
                    accumulated_data.append(row_data)

                yield accumulated_data


if __name__ == "__main__":

    def run_data_fetcher(fetcher):
        while True:
            try:
                fetched_data = next(fetcher)
                print(len(fetched_data))
                time.sleep(10)
            except StopIteration:
                print("Generator is terminated!")
                break
        print("finish of data fetcher, bye~~")


    kafka_daq = KafkaDataAcquisitor(
        data_acq_name='kafka_1',
        bootstrap_server='localhost:9092',
        topic='testTopic'
    )

    run_kafka_daq_thread = threading.Thread(target=kafka_daq.run)
    # run_kafka_data_fetcher = threading.Thread(target=kafka_daq.get_data)
    print("go to run daq")
    run_kafka_daq_thread.start()
    data_fetcher = kafka_daq.get_data_fetcher()

    run_kafka_data_fetcher = threading.Thread(target=run_data_fetcher, kwargs={"fetcher": data_fetcher})
    run_kafka_data_fetcher.start()

    time.sleep(60)

    kafka_daq.stop()


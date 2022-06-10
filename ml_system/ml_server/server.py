import threading

from data_acq_controller import DataAcquisitorController

from ml_system.tools.data_aquisitor import KafkaDataAcquisitor
from ml_system.ml_server.data_acq_servicer import DataAcquisitorServicer

from ml_system.tools.model import SklearnRandonForest


class MachineLearningServer:

    """
    Machine Learning System implements AI/ML Solutions as software system
    Which is consisted by following functionalities
    1. Data Ingress
    2. AI/ML Model Training
    3. AI/ML Model Serving
    4. Model performance inspection
    5. Controlling various pipeline w.r.t. Model action.

    MachineLearningServer is designed as main process which holding on various controller and servicer.
    The controller is responsible for coordinating object, i.e. the interface between server and various objects.
    including 1. Model; 2. Data Acquisitor.
    The servicer is responsible for maintain the core parts of AI/ML services.
    including 1. Data Acquisition services; 2. Model Training services; 3. Model Inference Serving; 4. Performance Monitor.



    """

    def __init__(self):

        # Controller
        self.__data_acq_controller = DataAcquisitorController.get_instance()
        self.__data_acq_servicer = None
        self.__model_controller = None
        self.__model_serving = None

        #TODO temporary experiment model object, should be removed in the future and using model_controller
        self._model = None
        # Servicer


        # repository
        self.__handling_data_acq = {}
        self.__handling_model_list = {}

        #init object needed
        self._init_data_daq()
        self._init_model()




    def _init_model(self, *args, **kwargs):
        self._model = SklearnRandonForest()


    def _init_data_daq(self):

        self.__data_acq_controller.create_data_acq(
            data_source_type='kafka',
            data_acq_name='kafka_1',
            bootstrap_server='localhost:9092',
            topic='testTopic'
        )


    def run(self):

        data_acq = self.__data_acq_controller.get_data_acq('kafka_1')
        self.__data_acq_servicer = DataAcquisitorServicer(data_acq)
        self.__data_acq_servicer.start()

        # data_acq_services = threading.Thread(target=data_acq.run)
        # data_acq_services.start()
        data_fetcher = data_acq.get_data()
        while True:
            try:
                print(next(data_fetcher))
            except StopIteration:
                print('Stop data acq')

if __name__ == '__main__':

    mls = MachineLearningServer()
    mls.run()



    # #TODO: implement model
    # def _start_training_model(self):
    #
    #     self._model = None
    #
    #     data = self._data_fetcher.get_data()
    #     self._model.fit(data)


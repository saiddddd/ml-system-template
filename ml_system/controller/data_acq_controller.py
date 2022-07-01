from ml_system.tools.data_aquisitor import KafkaDataAcquisitor
from ml_system.servicer.data_ingress_servicer import DataAcquisitorServicer


class DataAcquisitorController:
    """
    DataAcquisitor Controller is responsible for manage Data ACQ object. Managing both data_acquisitor and servicer.
    * DataAcquisitor : Entity for
    DataAcquisitorController is designed as singleton,
    one and only one controller will be used in ml system.
    Only Operated by ml server main process
    """

    # design in singleton pattern
    _instance = None

    @staticmethod
    def get_instance():
        if DataAcquisitorController._instance is None:
            DataAcquisitorController._instance = DataAcquisitorController()
        return DataAcquisitorController._instance

    def __init__(self):

        # internal repository for holding data acq
        self.__data_acq_repository = {}  # data acquisitor object is registered here
        self.__data_acq_servicer_repository = {}  # start to run data acquisitor execution job is registered here

    def create_data_acq(self, data_source_type: str, data_acq_name: str, *args, **kwargs):
        if data_source_type == 'kafka':

            data_daq = KafkaDataAcquisitor(
                data_acq_name=data_acq_name,
                bootstrap_server=kwargs.get('bootstrap_server'),
                topic=kwargs.get('topic')
            )
            self.__data_acq_repository[data_acq_name] = data_daq


    def get_data_acq(self, data_acq_name: str) -> object:
        return self.__data_acq_repository.get(data_acq_name)


    def _create_data_acq_by_servicer(self, data_acq_name: str):
        try:
            data_acq = self.__data_acq_repository.get(data_acq_name)
        except Exception:
            print("do not found data acq: {} from register! please create data acq first!!")

        data_acq_servicer = DataAcquisitorServicer(data_acq)
        self.__data_acq_servicer_repository[data_acq_name+'_servicer'] = data_acq_servicer
        print('create data acq: {} servicer successfully'.format(data_acq_name))

    def run_data_acq_by_servicer(self, data_acq_name: str, auto_retry_times: int):

        data_acq_servicer = self.__data_acq_servicer_repository.get(data_acq_name + '_servicer')

        if data_acq_servicer is None:

            print('data_acq_servicer not registered. Creating servicer now!')
            self._create_data_acq_by_servicer(data_acq_name)
            print('create data acq servicer successfully')
            data_acq_servicer = self.__data_acq_servicer_repository.get(data_acq_name+'_servicer')

        print('check data acq servicer')
        data_acq_servicer.start()







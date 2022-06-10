from ml_system.tools.data_aquisitor import KafkaDataAcquisitor


class DataAcquisitorController:
    """
    DataAcquisitor Controller is responsible for manage Data ACQ object.
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
        self.__data_acq_repository = {}

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



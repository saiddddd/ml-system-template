
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

    def get_data_acq(self, data_acq_name: str) -> object:
        return self.__data_acq_repository.get(data_acq_name)

    def save_data_acq_into_repository(self, data_acq_name: str, data_acq: object):
        self.__data_acq_repository[data_acq_name] = data_acq


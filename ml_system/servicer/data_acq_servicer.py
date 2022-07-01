from threading import Thread

from ml_system.tools.data_aquisitor import DataAcquisitor


class DataAcquisitorServicer:

    def __init__(self, data_acquisitor: DataAcquisitor):

        self._data_acquisitor = data_acquisitor
        self._data_acquisitor_service = Thread(target=self._data_acquisitor.run)
        self._running_status = None

    def start(self):
        """
        Start to execute data_acq run method
        The data_acq status will be noted as `running` while run() method going
        :return:
        """
        self._data_acquisitor_service.start()

    def stop(self):
        """
        data_acq stop by noted status as `stopped`
        the data_acq run method will be terminated and the run thread will be joined back.
        :return:
        """
        self._data_acquisitor.stop()
        self._data_acquisitor_service.join()

    def get_data_acq_status(self):
        return self._data_acquisitor.data_acquisitor_status

from threading import Thread

from ml_system.tools.data_aquisitor import DataAcquisitor


class DataAcquisitorServicer:

    def __init__(self, data_acquisitor: DataAcquisitor):

        self._data_acquisitor = data_acquisitor
        self._data_acquisitor_service = Thread(target=self._data_acquisitor.run)
        self._running_status = None

    def start(self):
        self._data_acquisitor_service.start()

    def stop(self):
        self._data_acquisitor.stop()
        self._data_acquisitor_service.join()

    def get_data_acq_status(self):
        return self._data_acquisitor.data_acquisitor_status

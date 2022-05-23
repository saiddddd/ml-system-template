

class MachineLearningServer:

    def __init__(self):

        # Controller
        self.__data_acq_controller = None
        self.__model_controller = None
        self.__model_serving = None

        # repository
        self.__handling_data_acq = {}
        self.__handling_model_list = {}


    def init_model(self, model_name: str, model, *args, **kwargs):
        raise NotImplementedError


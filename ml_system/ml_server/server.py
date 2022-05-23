

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
        self.__data_acq_controller = None
        self.__model_controller = None
        self.__model_serving = None

        # Servicer


        # repository
        self.__handling_data_acq = {}
        self.__handling_model_list = {}



    def init_model(self, model_name: str, model, *args, **kwargs):
        raise NotImplementedError


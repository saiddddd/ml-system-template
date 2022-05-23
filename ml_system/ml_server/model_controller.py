

class ModelController:
    """
    Model Controller is responsible for coordinating models which have been used.
    ModelController is design in singleton pattern,
    Online ML system has one and only one ModelController.
    Only Operated by ML server main process.
    """

    # design in singleton pattern
    _instance = None

    @staticmethod
    def get_instance():
        if ModelController._instance is None:
            ModelController._instance = ModelController()
        return ModelController._instance

    def __init__(self):

        # m
        self.__model_repository = {}

    def get_model_from_repository(self, model_name: str) -> object:
        """
        get model from repository by name
        :param model_name:
        :return:
        """
        return self.__model_repository.get(model_name)

    def save_model_into_repository(self, model_name: str, model: object):
        self.__model_repository[model_name] = model

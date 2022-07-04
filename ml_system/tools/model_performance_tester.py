
from abc import ABC
import pandas as pd
import os
from tqdm import tqdm
import pickle

class ModelTester(ABC):

    def __init__(self):
        self._model = None
        self._testing_data_path_list = []
        self._label = ''

    def set_model(self, model: object):
        self._model = model
        return self

    def set_testing_dataset(self, testing_data_path: list):
        for f in testing_data_path:
            if os.path.isfile(f):
                pass
            else:
                raise FileNotFoundError('The file {} in the provided list not found!, please check'.format(f))
        self._testing_data_path_list = testing_data_path
        return self

    def set_label(self, label: str):
        self._label = label





class OnlineMLPredictor(ModelTester):

    def __init__(self):
        super(OnlineMLPredictor).__init__()

    def run_predict(self):

        for f in self._testing_data_path_list:
            print(f)

            df = pd.read_csv(f)
            y = df.pop(self._label)

            predict_is_true = []

            for index, row in tqdm(df.iterrows(), total=df.shape[0]):


                predict_result = self._model.predict_proba_one(row)
                if isinstance(predict_result, dict):
                    if predict_result.get(1) > 0.5:
                        predict_is_true.append(1)
                    else:
                        predict_is_true.append(0)

            yield predict_is_true, y


# class OnlineMLTestRunner(ModelTester, OnlineMLPredictor):
#
#     def __init__(self):
#         super(OnlineMLTestRunner).__init__()
#
#
#     def run_model_tester(self):
#
#         while True:
#             predict_is_true, y = next(self.run_predict())
#
#             print(predict_is_true, y)

        # for f in self._testing_data_path_list:
        #     df = pd.read_csv(f)
        #     y = df.pop(self._label)
        #
        #     predict_is_true = []
        #
        #     for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        #
        #
        #         predict_result = self._model.predict_proba(row)
        #         if isinstance(predict_result, dict):
        #             if predict_result.get(1) > 0.5:
        #                 predict_is_true.append(1)
        #             else:
        #                 predict_is_true.append(0)
        #
        #     yield predict_is_true, y

if __name__ == '__main__':
    data_path_list = [
        '../../data/dummy/dummy_data_testing_1.csv',
        '../../data/dummy/dummy_data_testing_2.csv'
    ]
    with open('/Users/pwang/BenWork/OnlineML/onlineml/model_store/pretrain_model_persist/testing_hoeffding_tree_pretrain_model.pickle', 'rb') as f:
        model = pickle.load(f)
    model_tester = OnlineMLPredictor()

    model_tester\
        .set_model(model)\
        .set_testing_dataset(data_path_list)\
        .set_label('Y')

    for pred_list, y in model_tester.run_predict():
        print(pred_list)
        print(y)






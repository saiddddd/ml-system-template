
import os

from abc import ABC

import pandas as pd
from sklearn.preprocessing import LabelEncoder


class DataLoader(ABC):

    def __init__(self, input_data_path):
        """
        Abstraction of DataLoader for reading from static data.
        Different from DataAcquisitor, here is basically reading static data from file or DB table.
        :param input_data_path:
        """

        self._data_path = input_data_path

    @staticmethod
    def __check_data_path_valid(data_path):
        """
        look up the provided data path is valid or not,
        implement in concrete object.
        :return:
        """
        raise NotImplementedError

    def get_df(self, do_label_encoder: True):

        raise NotImplementedError


class CsvDataLoader(DataLoader):

    def __init__(self, *args, **kwargs):
        """
        implementation of data loader which responsible for csv file.

        :param args:
        :param kwargs:
        """

        # check of input file is acceptable
        data_path = kwargs.get('data_path')
        self.__check_data_path_valid(data_path)

        super(CsvDataLoader, self).__init__(data_path)

        self._df = pd.read_csv(self._data_path)

    @staticmethod
    def __check_data_path_valid(data_path):
        """
        check the provided data path is existed, and it is csv file
        :return:
        """

        if os.path.isfile(data_path):
            if data_path.split('.')[-1] != 'csv':
                raise RuntimeError('provided file {} is not csv'.format(data_path))
        else:
            raise FileNotFoundError('provided file {} is not exist'.format(data_path))



    def _do_label_encoder(self):
        for col in self._df.columns:
            if self._df[col].dtype == 'object':
                self._df[col] = self._df[col].fillna(self._df[col].mode())
                self._df[col] = LabelEncoder().fit_transform(self._df[col])
            else:
                self._df[col] = self._df[col].fillna(self._df[col].median())

    def get_df(self, do_label_encoder: True):
        """
        provide dataframe read from csv
        encoding string object by sklearn LabelEncoder
        fill na as well
        :return:
        """

        print("going to get df")

        if do_label_encoder:
            self._do_label_encoder()

        return self._df


    def show_dataframe(self, row_limit):
        print(self._df.head(row_limit))


if __name__ == '__main__':

    loader = CsvDataLoader(data_path='/Users/pwang/BenWork/OnlineML/onlineml/data/airline/airline_data.csv')
    loader.show_dataframe(row_limit=100)


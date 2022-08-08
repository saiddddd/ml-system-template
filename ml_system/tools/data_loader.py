
import os

from abc import ABC

import pandas
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler

from collections import Counter


class DataLoader(ABC):

    def __init__(self, input_data_path):
        """
        Abstraction of DataLoader for reading from static data.
        Different from DataAcquisitor, here is basically reading static data from file or DB table.
        :param input_data_path:
        """

        self._raw_df = None
        self._df_x = None
        self._df_y = None
        self._resample_df_x = None
        self._resample_df_y = None

        self._data_path = input_data_path

    @staticmethod
    def __check_data_path_valid(data_path):
        """
        look up the provided data path is valid or not,
        implement in concrete object.
        :return:
        """
        raise NotImplementedError

    def _load_df(self):
        raise NotImplementedError

    def _do_label_encoder(self):
        for col in self._raw_df.columns:
            if self._raw_df[col].dtype == 'object':
                self._raw_df[col] = self._raw_df[col].fillna(self._raw_df[col].mode())
                self._raw_df[col] = LabelEncoder().fit_transform(self._raw_df[col].astype('str'))
            else:
                self._raw_df[col] = self._raw_df[col].fillna(self._raw_df[col].median())


    def get_df(self, do_label_encoder: True, random_sampling=-1):
        self._load_df()
        if do_label_encoder:
            self._do_label_encoder()

        if random_sampling == -1:
            return self._raw_df
        else:
            return self._raw_df.sample(n=random_sampling)


    def get_df_x_y(self, label='', do_label_encoder=True, random_sampling=-1) -> (pandas.DataFrame, pandas.DataFrame):

        try:
            self._df_x = self.get_df(do_label_encoder=do_label_encoder, random_sampling=random_sampling)
            self._df_y = self._df_x.pop(label)

        except:
            print("label {} Not found from df".format(label))
            print(self._df_x)

        return self._df_x, self._df_y

    def get_resample_x_y(self, label='', do_label_encoder=True, resampler=RandomUnderSampler(random_state=42, sampling_strategy='auto')):
        """
        resampler using imblearn module's member,
        here can be RandomUnderSampler or RandomOverSampler
        :param label:
        :param resampler:
        :param do_label_encoder:
        :param random_sampling:
        :return:
        """

        if resampler is not None:
            df_x, df_y = self.get_df_x_y(label=label, do_label_encoder=do_label_encoder)
            print(df_x)
            resample_df_x, resample_df_y = resampler.fit_resample(df_x, df_y)


            print("successfully done with data resampling")
            print("The shape of original dataframe: {}".format(sorted(Counter(df_y).items())))
            print("The shape after resampling: {}".format(sorted(Counter(self._resample_df_y).items())))

            print(self._resample_df_x)
            print(self._resample_df_y)

            return self._resample_df_x, self._resample_df_y

        else:
            print("please specify the data resampler, imblearn under sampler or over sampler ..")



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

    def _load_df(self):
        self._raw_df = pd.read_csv(self._data_path)

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



    # def _do_label_encoder(self):
    #     for col in self._df.columns:
    #         if self._df[col].dtype == 'object':
    #             self._df[col] = self._df[col].fillna(self._df[col].mode())
    #             self._df[col] = LabelEncoder().fit_transform(self._df[col].astype('str'))
    #         else:
    #             self._df[col] = self._df[col].fillna(self._df[col].median())

    # def get_df(self, do_label_encoder: True):
    #     """
    #     provide dataframe read from csv
    #     encoding string object by sklearn LabelEncoder
    #     fill na as well
    #     :return:
    #     """
    #
    #     print("going to get df")
    #
    #     self._load_df()
    #
    #     if do_label_encoder:
    #         self._do_label_encoder()
    #
    #     return self._df


    def show_dataframe(self, row_limit):
        print(self._df.head(row_limit))


if __name__ == '__main__':

    loader = CsvDataLoader(data_path='/Users/pwang/BenWork/OnlineML/onlineml/data/airline/airline_data.csv')
    loader.show_dataframe(row_limit=100)


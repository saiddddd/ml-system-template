from ml_system.tools.data_loader import CsvDataLoader
from imblearn.over_sampling import RandomOverSampler

def test_get_df():

    csv_loader = CsvDataLoader(data_path='../data/hospital/aggregate_data.csv')
    df = csv_loader.get_df(do_label_encoder=True)
    print(df.shape[0])

def test_get_df_x_y():

    csv_loader = CsvDataLoader(data_path='../data/hospital/aggregate_data.csv')
    df_x, df_y = csv_loader.get_df_x_y(label='SEPSIS', do_label_encoder=True, random_sampling=10)
    print(df_x.shape[0])

def test_get_resample_x_y():
    csv_loader = CsvDataLoader(data_path='../data/hospital/aggregate_data.csv')

    resampler = RandomOverSampler(random_state=42, sampling_strategy='auto')
    x, y = csv_loader.get_resample_x_y(label="SEPSIS", do_label_encoder=True, resampler=resampler, random_sampling=10)
    print(x)
    print(y)
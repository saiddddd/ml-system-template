# ml-system-template
The prototype of ml system template for doing ml pipeline in services.

## Introduction
Machine Learning System implements AI/ML Solutions as software system
Which is consisted by following functionalities
1. Data Ingress
2. AI/ML Model Training
3. AI/ML Model Serving
4. Model performance inspection
5. Controlling various pipeline w.r.t. Model action.

MachineLearningServer is designed as main process which holding on various controller and servicer.
The controller is responsible for coordinating object, i.e. the interface between server and various objects.
including:
1. Model
2. Data Acquisitor.

The servicer is responsible for maintain the core parts of AI/ML services.
including: 
1. Data Acquisition services
2. Model Training services
3. Model Inference Serving
4. Performance Monitor.

__Sections__:
* __Data Ingress__
* __Machine Learning__
* __Model Serving__
* __Model Performance Inspection__

## __Data Ingress__

Generally, when people dealing with AI/ML projects, will use the module named `data_loader`, but here I introduce `ingress` to represent the idea on top of data loading process. The data ingress includes two processes, one is the general `data_loader`, and the other is `data_acquisitor`. For `data_loader`, which is put in charged for loading data from static data storage, e.g., the data base, file system, or local file objects, etc. On the other hand, the data acquisitor plays the role of streaming data ingress pump. Designing in listen public api to extract open data source, or fetching data from Kafka system. Streaming can be applied on one-pass learning features, i.e. online-machine-learning. Or continuously dumping streaming data into disk for traditional ML processes.

![introduction to data ingress process](/docs/figures/introduction_to_data_ingress.png)

### DataLoader

Here design data loader to responsible for read data from static file. Dealing with DataLoader, which is an abstraction, for all type of data. Based on requirements, the concrete implement is design. For example, reading data from CSV file using `CsvDataLoader` to get pandas dataframe. 
> csv_loader = CsvDataLoader(data_path="_data path_")  
> df = csv_loader.get_df() # return pandas dataframe  

In the case of extraction of X Y dataframe separation. Using following method
> csv_loader = CsvDataLoader(data_path="_data_path_")  
> df_x, df_y = csv_loader.get_df_x_y(label='_LABEL_COLUMN_NAME_')  

to get training dataset `df_x` and label series `df_y` by provided label column name.

If resampling is needed, use following method.
> from imblearn.over_sampling import RandomOverSampler, RandomUnderSampler  
> csv_loader = CsvDataLoader(data_path="_data_path_")  
> resampler = RandomOverSampler(random_state=42, sampling_strategy='auto')  
> x, y = csv_loader.get_resample_x_y(label="_LABEL_COLUMN_NAME_", resampler=resampler)  
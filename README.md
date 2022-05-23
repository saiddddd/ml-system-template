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

Generally, while people dealing with AI/ML project, will use the module named as `data_loader`, but here I introduce `ingress` as represent the idea on top of data loading process. The data ingress includes two processes, one is the general `data_loader`, and the other is `data_acquisitor`. For `data_loader`, which is put in charged for loading data from static data storage, e.g., the data base, file system, or local file objects, etc. On the other hand, data acquisitor is role as streaming data ingress pump. Designing in listen public api to extract open data source, or fetching data from Kafka system. Streaming can be applied on one-pass learning features, i.e. online-machine-learning. Or continuously dumping streaming data into disk for traditional ML processes.

![introduction to data ingress process](/docs/figures/introduction_to_data_ingress.png)
# IA-Knoxly
This repository conteins the dataset and the script used to build the AI of Knoxly.  

## What is Knoxly
Knoxy is a Google Chrome plug-in that allows you to highlight sensitive data based on dictionaries and regexp.
In this repo I build an IA for Knoxly able to recognize context-dependent sensitive data.  
Sensitive data that can identify AI relate to the following topics:
- **politics**
- **health**
- **job**
- **travel**
- **general**


## Prerequisites
To run this model you need:
|        Package       |  Version  |
|:--------------------:|:---------:|
|        pandas        |   1.0.1   |
|       matpotlib      |   3.1.3   |
|         numpy        |   1.18.1  |
|         regex        | 2020.2.20 |
|   sentence-splitter  |    1.4    |
|        sklearn       |    0.0    |
|         scipy        |   1.4.1   |
|      tensorflow      |   2.1.0   |
| tensorflow-estimator |   2.1.0   |
|    tensorflow-hub    |   0.7.0   |
|    tensorflow-text   |   2.1.1   |
|       textblob       |   0.15.3  |

## The data
To identify the following topics, a classifier has been trained to take data from the following datasets.
- [Election day tweet](https://www.kaggle.com/kinguistics/election-day-tweets?rvi=1)
- [Medical Transcript](https://www.kaggle.com/tboyle10/medicaltranscriptions?rvi=1)
- [Medical speech transcript and intent](https://www.kaggle.com/paultimothymooney/medical-speech-transcription-and-intent?rvi=1)
- [Amazon job skills](https://www.kaggle.com/atahmasb/amazon-job-skills?rvi=1)
- [Twitter airline sentiment](https://www.kaggle.com/crowdflower/twitter-airline-sentiment?rvi=1)
- [The movie dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset)
The pre-processed dataset used to build the dataset are in [dataset folder](https://github.com/CiccioTecchio/IA-Knoxly/blob/master/dataset/ds.zip)

### Create dataset
to create the dataset to give input to the IA:
```bash
# 1. in a new folder extraxct ds.zip
# 2. move the python script named crea.py present in src/create_ds in the new folder
echo text,tipo >> ds1000.csv
python3 crea.py ds1000.csv 1000
echo text,tipo >> ds2000.csv #for wild testing
python3 crea.py ds2000.csv 2000
# move ds1000 & ds2000 in src
```

## Run topic classifier
```bash
python3 src/topic_class.py src/ds1000.csv 
```

## Run sensitiveness classifier
To run a sensitiveness classifier you need a new dataset with the label sensibile(1) not sensibile(0). The dataset is present in src and the name of the dataset is ds200.csv
```bash
python3 sensitiveness.py
```

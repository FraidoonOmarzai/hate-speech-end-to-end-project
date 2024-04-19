from src.exception import CustomException
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig
import sys
import os

import pandas as pd

import re
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


class DataTransformation:
    """Handles data transformation operations.

    This class performs data transformation operations such as data cleaning,
    concatenation of dataframes, and saving transformed data to a file.

    Attributes:
        data_transformation_config (DataTransformationConfig): Configuration object for data transformation.
        data_ingestion_artifact (DataIngestionArtifact): Artifact containing paths to ingested data.

    Methods:
        imbalanced_data: Processes and prepares the imbalanced data.
        raw_data: Processes and prepares the raw data.
        concat_df1_df2: Concatenates processed dataframes.
        data_cleaning: Cleans text data by removing HTML tags, stopwords, and applying stemming.
        init_data_transformation: Initializes the data transformation process.

    """

    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_config = data_transformation_config

    def imbalanced_data(self):
        try:
            logging.info("inside imbalanced_data function")
            # read the csv file
            df1 = pd.read_csv(
                self.data_ingestion_artifact.imbalanced_data_path)
            # remove the id column
            df1 = df1.drop(['id'], axis=1)
            # remove duplicates
            df1 = df1.drop_duplicates(keep='first')

            return df1

        except Exception as e:
            raise CustomException(e, sys)

    def raw_data(self):
        try:
            logging.info("inside raw_data function")
            # read the csv file
            df2 = pd.read_csv(self.data_ingestion_artifact.raw_data_path)
            # remove unnecessary columns
            df2 = df2.drop(['Unnamed: 0', 'count', 'hate_speech',
                           'offensive_language', 'neither'], axis=1)
            # copy the valus of the class 1 into class 0.
            # Let's copy the valus of the class 1 into class 0.
            class_1_values = df2[df2['class'] == 1]['class'].values
            class_0_indices = df2[df2['class'] == 0].index
            df2.loc[class_0_indices,
                    'class'] = class_1_values[:len(class_0_indices)]
            # Let's replace the value of 2 to 0.
            df2.replace({'class': {2: 0}}, inplace=True)
            # Let's change the name of the 'class' to label
            df2.rename(columns={'class': 'label'}, inplace=True)

            return df2

        except Exception as e:
            raise CustomException(e, sys)

    def data_cleaning_1(self, words):

        try:
            logging.info("Entered into the concat_data_cleaning function")
            # Let's apply stemming and stopwords on the data
            stemmer = nltk.SnowballStemmer("english")
            stopword = set(stopwords.words('english'))
            words = str(words).lower()
            words = re.sub('\[.*?\]', '', words)
            words = re.sub('https?://\S+|www\.\S+', '', words)
            words = re.sub('<.*?>+', '', words)
            words = re.sub('[%s]' % re.escape(string.punctuation), '', words)
            words = re.sub('\n', '', words)
            words = re.sub('\w*\d\w*', '', words)
            words = [word for word in words.split(
                ' ') if words not in stopword]
            words = " ".join(words)
            words = [stemmer.stem(word) for word in words.split(' ')]
            words = " ".join(words)
            logging.info("Exited the concat_data_cleaning function")
            return words

        except Exception as e:
            raise CustomException(e, sys) from e

    def init_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info('init_data_transformation starting')
            # load the concatenated data [df1, df2]
            # df = self.concat_df1_df2()

            df = self.imbalanced_data()
            # df= self.raw_data()
            # apply the data cleaning
            df['tweet'] = df['tweet'].apply(self.data_cleaning_1)

            os.makedirs(
                self.data_transformation_config.data_transformation_dir, exist_ok=True)
            df.to_csv(
                self.data_transformation_config.transformed_file, index=False, header=True)

            data_transformation_artifacts = DataTransformationArtifact(
                self.data_transformation_config.transformed_file
            )

            return data_transformation_artifacts
        except Exception as e:
            raise CustomException(e, sys)

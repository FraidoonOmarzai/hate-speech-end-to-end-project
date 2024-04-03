from src.exception import CustomException
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig
import sys
import os

import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk import SnowballStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


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
            CustomException(e, sys)

    def raw_data(self):
        try:
            logging.info("inside raw_data function")
            # read the csv file
            df2 = pd.read_csv(self.data_ingestion_artifact.raw_data_path)
            # remove unnecessary columns
            df2 = df2.drop(['Unnamed: 0', 'count', 'hate_speech',
                           'offensive_language', 'neither'], axis=1)
            # copy the valus of the class 1 into class 0.
            df2[df2['class'] == 0]['class'] = 1
            # replace the value of 0 to 1
            df2["class"].replace({0: 1}, inplace=True)
            # Let's replace the value of 2 to 0.
            df2["class"].replace({2: 0}, inplace=True)
            # Let's change the name of the 'class' to label
            df2.rename(columns={'class': 'label'}, inplace=True)

            return df2

        except Exception as e:
            CustomException(e, sys)

    def concat_df1_df2(self):
        try:
            logging.info('inside concat_df1_df2 function')
            df1 = self.imbalanced_data()
            df2 = self.raw_data()

            # Let's concatinate both the data into a single data frame.
            frame = [df1, df2]
            df = pd.concat(frame)

            return df

        except Exception as e:
            CustomException(e, sys)

    def data_cleaning(self, txt, stemmer=SnowballStemmer("english"), stop_words=set(stopwords.words('english'))):
        try:
            # remove html tags
            soup = BeautifulSoup(txt, 'html.parser')
            clean_text = soup.get_text()

            # convert to lower case and splits up the words
            words = word_tokenize(clean_text.lower())

            filter_words = []

            for word in words:
                # removing the stop words and punctuation
                if word not in stop_words and word.isalpha():
                    filter_words.append(stemmer.stem(word))  # words stemming

            return ' '.join(filter_words)
        except Exception as e:
            CustomException(e, sys)

    def init_data_transformation(self):
        try:
            logging.info('init_data_transformation starting')
            # load the concatenated data [df1, df2]
            df = self.concat_df1_df2()
            # apply the data cleaning
            df['tweet'] = df['tweet'].apply(self.data_cleaning)

            os.makedirs(
                self.data_transformation_config.data_transformation_dir, exist_ok=True)
            df.to_csv(
                self.data_transformation_config.transformed_file, index=False, header=True)

            data_transformation_artifacts = DataTransformationArtifact(
                self.data_transformation_config.transformed_file
            )

            return data_transformation_artifacts
        except Exception as e:
            CustomException(e, sys)

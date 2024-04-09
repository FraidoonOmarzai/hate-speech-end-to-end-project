from src.exception import CustomException
from src.logger import logging
from src.entity.artifact_entity import ModelTrainingArtifact, DataTransformationArtifact
from src.entity.config_entity import ModelTrainingConfig

import sys
import os

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split

import tensorflow
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

from src.ml.model import ModelArchitecture


class ModelTraining:
    def __init__(self,
                 data_transformer_artifact: DataTransformationArtifact,
                 model_training_config: ModelTrainingConfig):
        self.data_transformer_artifact = data_transformer_artifact
        self.model_training_config = model_training_config

    def data_split(self):
        try:
            logging.info("data splitting...")
            df = pd.read_csv(self.data_transformer_artifact.df_file)
            X = df[self.model_training_config.tweet]
            y = df[self.model_training_config.label]
            X_train,X_test,y_train,y_test = train_test_split(
                X, y, random_state=42)

            return X_train,X_test,y_train,y_test

        except Exception as e:
            raise CustomException(e, sys)

    def tokenizaiton(self, X_train):
        try:
            logging.info("Applying tokenization on the data")
            tokenizer = Tokenizer(num_words=self.model_training_config.max_words,
                                  lower=False)
            tokenizer.fit_on_texts(X_train)
            sequences = tokenizer.texts_to_sequences(X_train)
            logging.info(f"converting text to sequences: {sequences}")
            sequences_matrix = pad_sequences(sequences,maxlen=self.model_training_config.max_length)
            logging.info(f" The sequence matrix is: {sequences_matrix}")
            return sequences_matrix,tokenizer

        except Exception as e:
            raise CustomException(e, sys)

    def init_model_training(self) -> ModelTrainingArtifact:
        try:
            X_train,X_test,y_train,y_test = self.data_split()

            tokenizer, sequences_matrix = self.tokenizaiton(X_train)
            
            logging.info('Initializing model training')
            model_arc = ModelArchitecture()
            lstm_model = model_arc.lstm_model()
            print(model_arc)

            logging.info('model training...')
            lstm_model.fit(sequences_matrix,
                            y_train,
                            batch_size=32,
                            epochs = 1,
                            validation_split=0.2)

            with open('tokenizer.pickle', 'wb') as text_vec:
                pickle.dump(tokenizer, text_vec,
                            protocol=pickle.HIGHEST_PROTOCOL)

            os.makedirs(
                self.model_training_config.model_training_dir, exist_ok=True)

            pickle.dump(
                lstm_model, self.model_training_config.training_model_path)
            
            
            X_test.to_csv(self.model_training_config.X_test_path)
            y_test.to_csv(self.model_training_config.y_test_path)
            
            
            model_training_artifacts = ModelTrainingArtifact(
                model_path = self.model_training_config.training_model_path,
                X_test_path = self.model_training_config.X_test_path,
                y_test_path = self.model_training_config.y_test_path
            )

            return model_training_artifacts
        except Exception as e:
            raise CustomException(e, sys)

from src.logger import logging
from src.exception import CustomException
from src.cloud_storage.s3_operations import S3Operation
from src.constants import *
from src.components.data_transformation import DataTransformation
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pickle
import keras
from keras.utils import pad_sequences


class PredictionPipeline:
    """A class for running prediction pipeline using a trained model.

    Attributes:
        bucket_name (str): The name of the S3 bucket where the best model is stored.
        best_model_dir (str): The directory path within the S3 bucket where the best model is located.
        model_name (str): The name of the best model file.
        model_path (str): The local directory path where the best model will be downloaded.
        s3_operation (S3Operation): An instance of the S3Operation class for interacting with S3.
        data_transformation (DataTransformation): An instance of the DataTransformation class for data preprocessing.

    Methods:
        get_model_from_s3(): Download the best model from S3 and return the local path.
        predict(best_model_path: str, text: str): Make a prediction on the provided text using the best model.
        run_pipeline(text: str): Run the prediction pipeline on the provided text.

    """

    def __init__(self):
        self.bucket_name = BUCKET_NAME
        self.best_model_dir = BEST_MODEL_DIR
        self.model_name = MODEL_NAME
        self.model_path = os.path.join("artifacts", "PredictModel")
        self.s3_operation = S3Operation()
        self.data_transformation = DataTransformation(data_transformation_config=DataTransformationConfig,
                                                      data_ingestion_artifact=DataIngestionArtifact)

    def get_model_from_s3(self) -> str:
        try:
            logging.info("Loading the best model from s3 bucket")
            os.makedirs(self.model_path, exist_ok=True)
            self.s3_operation.sync_folder_from_s3(self.model_path,
                                                  self.bucket_name,
                                                  self.best_model_dir)
            best_model_path = os.path.join(self.model_path, self.model_name)
            logging.info("Best model downloaded from s3 bucket")
            return best_model_path

        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, best_model_path, text):
        logging.info("Running the predict function")
        try:
            load_model = keras.models.load_model(best_model_path)
            with open('tokenizer.pickle', 'rb') as handle:
                load_tokenizer = pickle.load(handle)

            text = self.data_transformation.data_cleaning_1(text)
            text = [text]
            # print(text)
            seq = load_tokenizer.texts_to_sequences(text)
            padded = pad_sequences(seq, maxlen=MAX_LENGTH)
            # print(seq)
            pred = load_model.predict(padded)
            pred
            print("pred", pred)
            if pred > 0.5:
                print("hate and abusive")
                return "hate and abusive"
            else:
                print("no hate")
                return "no hate"
        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self, text):
        try:
            logging.info("Running prediction pipeline")
            best_model_path: str = self.get_model_from_s3()
            predicted_text = self.predict(best_model_path, text)
            logging.info("Prediction done")
            return predicted_text
        except Exception as e:
            raise CustomException(e, sys) from e

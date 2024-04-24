from src.logger import logging
from src.exception import CustomException
from src.constants import *
from src.entity.artifact_entity import ModelTrainingArtifact, ModelEvaluationArtifact
from src.entity.config_entity import ModelEvaluationConfig
from src.cloud_storage.s3_operations import S3Operation

import os
import sys
import pickle
import pandas as pd
import keras
from keras.utils import pad_sequences
from sklearn.metrics import confusion_matrix


class ModelEvaluation:
    def __init__(self,
                 model_training_artifacts: ModelTrainingArtifact,
                 model_evaluation_config: ModelEvaluationConfig):
        self.model_training_artifacts = model_training_artifacts
        self.model_evaluation_config = model_evaluation_config
        self.s3operation = S3Operation()

    def evaluation(self):
        try:

            logging.info("loading tokenizer...")
            with open('tokenizer.pickle', 'rb') as tex_vec:
                tokenizer = pickle.load(tex_vec)

            logging.info("loading X_test, y_test and model")
            X_test = pd.read_csv(
                self.model_training_artifacts.X_test_path, index_col=0)
            y_test = pd.read_csv(
                self.model_training_artifacts.y_test_path, index_col=0)
            model = keras.models.load_model(
                self.model_training_artifacts.model_path)

            X_test = X_test['tweet'].astype(str)
            X_test = X_test.squeeze()
            y_test = y_test.squeeze()

            test_sequence = tokenizer.texts_to_sequences(X_test)
            test_sequence_matrix = pad_sequences(
                test_sequence, maxlen=MAX_LENGTH)

            print(test_sequence_matrix)

            accuracy = model.evaluate(test_sequence_matrix, y_test)

            print(f'Accuracy: {accuracy}')

            lstm_prediction = model.predict(test_sequence_matrix)
            res = []
            for prediction in lstm_prediction:
                if prediction[0] < 0.5:
                    res.append(0)
                else:
                    res.append(1)
            print(confusion_matrix(y_test, res))
            logging.info(
                f"the confusion_matrix is {confusion_matrix(y_test,res)} ")
            return accuracy
        except Exception as e:
            raise CustomException(e, sys)

    def get_best_model_from_cloud(self):
        try:
            os.makedirs(
                self.model_evaluation_config.best_model_path, exist_ok=True)
            self.s3operation.sync_folder_from_s3(
                folder=self.model_evaluation_config.best_model_path,
                bucket_name=self.model_evaluation_config.bucket_name,
                bucket_folder_name=self.model_evaluation_config.best_model
            )

            best_model_path_dir = os.path.join(self.model_evaluation_config.best_model_path,
                                               self.model_evaluation_config.model_name)

            return best_model_path_dir

        except Exception as e:
            raise CustomException(e, sys)

    def init_model_evaluation(self):
        try:

            logging.info("Loading currently trained model")
            trained_model = keras.models.load_model(
                self.model_training_artifacts.model_path)
            with open('tokenizer.pickle', 'rb') as tex_vec:
                load_tokenizer = pickle.load(tex_vec)

            trained_model_accuracy = self.evaluation()

            logging.info("Fetch best model from gcloud storage")
            best_model_path = self.get_best_model_from_cloud()

            logging.info(
                "Check is best model present in the gcloud storage or not ?")
            if os.path.isfile(best_model_path) is False:
                is_model_accepted = True
                logging.info(
                    "glcoud storage model is false and currently trained model accepted is true")

            else:
                logging.info("Load best model fetched from gcloud storage")
                best_model = keras.models.load_model(best_model_path)
                best_model_accuracy = self.evaluation()

                logging.info(
                    "Comparing loss between best_model_loss and trained_model_loss ? ")
                if best_model_accuracy > trained_model_accuracy:
                    is_model_accepted = True
                    logging.info("Trained model not accepted")
                else:
                    is_model_accepted = False
                    logging.info("Trained model accepted")

            model_evaluation_artifacts = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted)
            logging.info("Returning the ModelEvaluationArtifacts")
            return model_evaluation_artifacts

        except Exception as e:
            raise CustomException(e, sys)

from src.exception import CustomException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTraining
from src.entity.config_entity import (DataIngestionConfig,
                                      DataTransformationConfig,
                                      ModelTrainingConfig)
from src.entity.artifact_entity import (DataIngestionArtifact,
                                        DataTransformationArtifact)

import sys


class TrainingPipeline:
    """Class representing a training pipeline.

    This class orchestrates the various steps involved in the training pipeline,
    including data ingestion, data transformation and further processing.

    Methods:
        start_data_ingestion: Starts the data ingestion process.
        start_data_transformation: Starts the data transformation process.
        run_pipeline: Runs the entire training pipeline.
    """

    def __init__(self) -> None:
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_training_config = ModelTrainingConfig()

    def start_data_ingestion(self):
        try:
            logging.info("starting data ingestion")
            data_ingestion = DataIngestion(
                self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.init_data_ingestion()

            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys)

    def start_data_transformation(self, data_ingestion_artifacts):
        try:
            logging.info("starting data transformation")
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifacts,
                data_transformation_config=self.data_transformation_config
            )

            data_transformation_artifacts = data_transformation.init_data_transformation()
            return data_transformation_artifacts

        except Exception as e:
            raise CustomException(e, sys)
            
            
    def start_model_training(self, data_transformation_artifacts):
        try:
            model_training = ModelTraining(
                data_transformer_artifact=data_transformation_artifacts,
                model_training_config=self.model_training_config
            )
            
            model_training.init_model_training()
            
        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self):
        logging.info("running training pipeline")
        try:
            # data ingestion Sections
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()

            # data Transformation Sections
            data_transformation_artifact: DataTransformationArtifact = self.start_data_transformation(
                data_ingestion_artifact)
            
            # Model Training Sections
            self.start_model_training(data_transformation_artifact)

        except Exception as e:
            raise CustomException(e, sys)

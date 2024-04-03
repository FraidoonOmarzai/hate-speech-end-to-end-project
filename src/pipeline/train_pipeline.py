from src.exception import CustomException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.entity.config_entity import (DataIngestionConfig,
                                    DataTransformationConfig,)
from src.entity.artifact_entity import (DataIngestionArtifact, 
                                        DataTransformationArtifact)

import sys


class TrainingPipeline:
    """Class representing a training pipeline.

    This class orchestrates the various steps involved in the training pipeline,
    including data ingestion and further processing.

    Methods:
        start_data_ingestion: Starts the data ingestion process.
        run_pipeline: Runs the entire training pipeline.
    """

    def __init__(self) -> None:
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()

    def start_data_ingestion(self):
        try:
            logging.info("starting data ingestion")
            data_ingestion = DataIngestion(
                self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.init_data_ingestion()

            return data_ingestion_artifact

        except Exception as e:
            CustomException(e, sys)
            
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
            CustomException(e, sys)

    def run_pipeline(self):
        logging.info("running training pipeline")
        try:
            # data ingestion sections
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            
            # data Transformation sections
            data_transformation_artifact: DataTransformationArtifact = self.start_data_transformation(data_ingestion_artifact)

        except Exception as e:
            CustomException(e, sys)

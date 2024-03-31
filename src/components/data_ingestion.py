from src.exception import CustomException
from src.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.cloud_storage.s3_operations import S3Operation
import sys


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.s3_operation = S3Operation()

    def get_data_from_s3(self) -> None:
        try:
            logging.info("downloading data from S3")

            self.s3_operation.sync_folder_from_s3(
                folder=self.data_ingestion_config.data_path,
                bucket_name=self.data_ingestion_config.bucket_name,
                bucket_folder_name=self.data_ingestion_config.s3_data_folder
            )
            logging.info('download completed')
        except Exception as e:
            CustomException(e, sys)

    def init_data_ingestion(self):
        try:
            logging.info("init_data_ingestion")
            
            self.get_data_from_s3()
            
            data_ingestion_artifact:DataIngestionArtifact = DataIngestionArtifact(
                zip_file=self.data_ingestion_config.zip_path
            )
            
            return data_ingestion_artifact
        
        except Exception as e:
            CustomException(e, sys)
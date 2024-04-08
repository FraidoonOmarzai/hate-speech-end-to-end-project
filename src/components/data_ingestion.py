from src.exception import CustomException
from src.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.cloud_storage.s3_operations import S3Operation
import sys
import zipfile


class DataIngestion:
    """Class for ingesting data from S3 and performing necessary operations.

    This class facilitates the process of downloading data from an S3 bucket,
    unzipping the downloaded data, and creating a data ingestion artifact.


    Methods:
        get_data_from_s3: Downloads data from S3 to the local system.
        unzip_data: Unzips the downloaded data.
        init_data_ingestion: Initializes the data ingestion process.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.s3_operation = S3Operation()

    def get_data_from_s3(self) -> None:
        try:
            logging.info("downloading data from S3")

            self.s3_operation.sync_folder_from_s3(
                folder=self.data_ingestion_config.data_ingestion_path,
                bucket_name=self.data_ingestion_config.bucket_name,
                bucket_folder_name=self.data_ingestion_config.s3_data_folder
            )
            logging.info('download completed')

        except Exception as e:
            raise CustomException(e, sys)

    def unzip_data(self):
        """function to unzip.

        returns:
            Tuple[str, str]: Paths to the unzipped data files (imbalanced data and raw data).
        """
        logging.info("unzipping data starting...")
        try:
            with zipfile.ZipFile(self.data_ingestion_config.zip_path, 'r') as zip_file:
                zip_file.extractall(self.data_ingestion_config.unzip_path)

            return self.data_ingestion_config.imbalanced_data, self.data_ingestion_config.raw_data
        except Exception as e:
            raise CustomException(e, sys)

    def init_data_ingestion(self):
        try:
            logging.info("init_data_ingestion")

            self.get_data_from_s3()
            imbalanced_data_path, raw_data_path = self.unzip_data()

            data_ingestion_artifact: DataIngestionArtifact = DataIngestionArtifact(
                imbalanced_data_path=imbalanced_data_path,
                raw_data_path=raw_data_path
            )

            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys)

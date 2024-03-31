from src.constants import *
import os


class DataIngestionConfig:
    """Data class for configuring data ingestion parameters.

    This class provides a convenient way to configure parameters related to data ingestion,
    such as directory paths and S3 bucket names.

    args:
        arificts_dir (str): The directory where artifacts are stored.
        s3_data_folder (str): The folder path within the S3 bucket containing the data.
        bucket_name (str): The name of the S3 bucket.
        data_path (str): The full path to the data within the artifacts directory.
        zip_path (str): The path to the zip file containing the data.
    """

    def __init__(self) -> None:
        self.arificts_dir = ARTIFACTS_DIR
        self.s3_data_folder = S3_DATA_FOLDER
        self.bucket_name = BUCKET_NAME

        self.data_path = os.path.join(
            self.arificts_dir, 'data_ingestion', self.s3_data_folder
        )

        self.zip_path = os.path.join(
            self.data_path, 'dataset.zip'
        )

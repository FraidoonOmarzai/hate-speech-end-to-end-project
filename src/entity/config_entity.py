from src.constants import *
import os


class DataIngestionConfig:
    """Data class for configuring data ingestion parameters.

    This class provides a convenient way to configure parameters related to data ingestion,
    such as directory paths and S3 bucket names.

    args:
        s3_data_folder (str): The folder path within the S3 bucket containing the data.
        bucket_name (str): The name of the S3 bucket.
        data_ingestion_path (str): The full path to the data within the artifacts directory.
        zip_path (str): The path to the zip file containing the data.
        unzip_path (str): The path to store the unzip files.
        imbalanced_data (str): The path to imbalance_data.cvs file.
        raw_data (str): The path to the raw_data.csv file.
    """

    def __init__(self) -> None:
        self.s3_data_folder = S3_DATA_FOLDER
        self.bucket_name = BUCKET_NAME

        self.data_ingestion_path = os.path.join(
            DATA_INGESTION_DIR, self.s3_data_folder)

        self.zip_path = os.path.join(DATA_INGESTION_DIR, 'dataset.zip')
        self.unzip_path = os.path.join(DATA_INGESTION_DIR)
        self.imbalanced_data = os.path.join(DATA_INGESTION_DIR, IMBALANCE_DATA)
        self.raw_data = os.path.join(DATA_INGESTION_DIR, RAW_DATA)


class DataTransformationConfig:
    """Data class for configuring data transformation parameters.

    This class provides a convenient way to configure parameters related to data transformation,
    such as directory paths.

    args:
        data_transformation_dir (str): The path to data transformation folder.
        transformed_file (str): The path to sotre the data after transformation.
    """

    def __init__(self):
        self.data_transformation_dir = os.path.join(DATA_TRANSFORM_DIR)
        self.transformed_file = os.path.join(
            self.data_transformation_dir, TRANSFORMED_FILE)


class ModelTrainingConfig:
    def __init__(self) -> None:
        self.model_training_dir = os.path.join(MODEL_TRAINING_DIR)
        self.tweet=TWEET
        self.label = LABEL
        self.max_words = MAX_WORDS
        self.max_length = MAX_LENGTH
        self.training_model_path = os.path.join(self.model_training_dir, MODEL_NAME)
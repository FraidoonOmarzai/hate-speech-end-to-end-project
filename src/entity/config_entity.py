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
        self.s3_file = S3_FILE

        self.data_ingestion_path = os.path.join(
            DATA_INGESTION_DIR, self.s3_data_folder)

        self.zip_path = os.path.join(
            DATA_INGESTION_DIR, self.s3_data_folder, self.s3_file)
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
    """A class to hold configuration parameters for model training.

    Args:
        - model_training_dir (str): Directory path where the model training data and outputs will be stored.
        - tweet (str): Name or path of the tweet data.
        - label (str): Name or path of the label data.
        - max_words (int): Maximum number of words to consider in the tokenization process.
        - max_length (int): Maximum length of a sequence to consider.
        - training_model_path (str): Path where the trained model will be saved.
        - X_test_path (str): Path where the test input data (features) will be stored.
        - y_test_path (str): Path where the test output data (labels) will be stored.
        - epochs (int): Number of epochs (iterations over the entire dataset) to train the model.
        - batch_size (int): Number of samples processed before the model is updated.
    """

    def __init__(self) -> None:
        self.model_training_dir = os.path.join(MODEL_TRAINING_DIR)
        self.tweet = TWEET
        self.label = LABEL
        self.max_words = MAX_WORDS
        self.max_length = MAX_LENGTH
        self.training_model_path = os.path.join(
            self.model_training_dir, MODEL_NAME)
        self.X_test_path = os.path.join(self.model_training_dir, X_TEST)
        self.y_test_path = os.path.join(self.model_training_dir, Y_TEST)
        self.epochs = EPOCHS
        self.batch_size = BATCH_SIZE


class ModelEvaluationConfig:
    def __init__(self):
        self.model_evaluation_dir = os.path.join(MODEL_EVALUATION_DIR)
        
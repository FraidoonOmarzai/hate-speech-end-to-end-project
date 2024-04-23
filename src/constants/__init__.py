from datetime import datetime
import os


# Common Constants
TIMESTAMP: datetime = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
ARTIFACTS_DIR: str = os.path.join('artifacts', TIMESTAMP)
BUCKET_NAME: str = 'hatedataset'
S3_DATA_FOLDER: str = 'data'
S3_FILE: str = 'dataset.zip'


# Data Ingestion Constants
DATA_INGESTION_DIR: str = os.path.join(ARTIFACTS_DIR, 'DataIngestion')
IMBALANCE_DATA: str = 'imbalanced_data.csv'
RAW_DATA: str = 'raw_data.csv'


# Data Transformation Constants
DATA_TRANSFORM_DIR: str = os.path.join(ARTIFACTS_DIR, 'DataTransformation')
TRANSFORMED_FILE: str = 'transforemd_df.csv'


# Model Training Constants
MODEL_TRAINING_DIR: str = os.path.join(ARTIFACTS_DIR, 'ModelTraining')
TWEET: str = 'tweet'
LABEL: str = 'label'
MODEL_NAME: str = 'model.h5'
X_TEST: str = 'X_test.csv'
Y_TEST: str = 'y_test.csv'

# tokenization
MAX_WORDS: int = 10000
MAX_LENGTH: int = 50

# model
EPOCHS: int = 1
BATCH_SIZE: int = 32


# Model Evaluation Constants
MODEL_EVALUATION_DIR = os.path.join(ARTIFACTS_DIR, 'ModelEvaluation')


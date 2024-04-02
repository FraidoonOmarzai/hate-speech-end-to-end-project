from datetime import datetime
import os


# Common Constants
TIMESTAMP: datetime = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
ARTIFACTS_DIR: str = os.path.join('artifacts', TIMESTAMP)
BUCKET_NAME: str = 'hatedataset'
S3_DATA_FOLDER: str = 'dataset.zip'


# Data Ingestion Constants
DATA_INGESTION_DIR: str = os.path.join(ARTIFACTS_DIR, 'DataIngestion')
IMBALANCE_DATA: str = 'imbalanced_data.csv'
RAW_DATA: str = 'raw_data.csv'

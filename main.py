from src.exception import CustomException
from src.pipeline.train_pipeline import TrainingPipeline
import sys

class StartTraining:
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        raise CustomException(e, sys)
        
if __name__ =="__main__":
    StartTraining()
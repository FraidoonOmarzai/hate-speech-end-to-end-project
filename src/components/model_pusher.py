from src.exception import CustomException
from src.logger import logging
from src.cloud_storage.s3_operations import S3Operation
from src.entity.config_entity import ModelPusherConfig
from src.entity.artifact_entity import ModelPusherArtifact
from src.entity.artifact_entity import ModelTrainingArtifact

import os
import sys

class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_training_artifact: ModelTrainingArtifact):
        self.model_pusher_config = model_pusher_config
        self.model_training_artifact = model_training_artifact
        self.s3_operation = S3Operation()
            
    
    def init_model_pusher(self):
        try:
            self.s3_operation.sync_folder_to_s3(self.model_training_artifact.model_path,
                                                self.model_pusher_config.bucket_name,
                                                self.model_pusher_config.best_model_dir)
            
            model_pusher_artifact = ModelPusherArtifact(
                self.model_pusher_config.bucket_name
            )
            
            return model_pusher_artifact
        except Exception as e:
            raise CustomException(e, sys)
        


    
    

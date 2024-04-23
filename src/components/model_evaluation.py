from src.logger import logging
from src.exception import CustomException
from src.constants import *
from src.entity.artifact_entity import ModelTrainingArtifact,ModelEvaluationArtifact
from src.entity.config_entity import ModelEvaluationConfig

import os
import sys
import pickle
import pandas as pd
import keras
from keras.utils import pad_sequences
from sklearn.metrics import confusion_matrix



class ModelEvaluation:
    def __init__(self,
                 model_training_artifacts:ModelTrainingArtifact,
                 model_evaluation_config: ModelEvaluationConfig):
        self.model_training_artifacts = model_training_artifacts
        self.model_evaluation_config = model_evaluation_config
        
        
    def evaluation(self):
        try:
            
            logging.info("loading tokenizer...")
            with open('tokenizer.pickle', 'rb') as tex_vec:
                tokenizer = pickle.load(tex_vec)
                
                
            logging.info("loading X_test, y_test and model")
            X_test = pd.read_csv(self.model_training_artifacts.X_test_path, index_col=0)
            y_test = pd.read_csv(self.model_training_artifacts.y_test_path, index_col=0)
            model = keras.models.load_model(self.model_training_artifacts.model_path)
            
            
            X_test = X_test['tweet'].astype(str)
            X_test = X_test.squeeze()
            y_test = y_test.squeeze()
            
            
            test_sequence = tokenizer.texts_to_sequences(X_test)
            test_sequence_matrix = pad_sequences(test_sequence, maxlen=MAX_LENGTH)
            
            print(test_sequence_matrix)
            
            accuracy = model.evaluate(test_sequence_matrix, y_test)
            
            print(f'Accuracy: {accuracy}')
        
            lstm_prediction = model.predict(test_sequence_matrix)
            res = []
            for prediction in lstm_prediction:
                if prediction[0] < 0.5:
                    res.append(0)
                else:
                    res.append(1)
            print(confusion_matrix(y_test,res))
            logging.info(f"the confusion_matrix is {confusion_matrix(y_test,res)} ")
            return accuracy
        except Exception as e:
            raise CustomException(e, sys)
        
    
    def init_model_evaluation(self):
        try:
            accuracy = self.evaluation()
            
            return accuracy
        except Exception as e:
            CustomException(e, sys)
        
        
        
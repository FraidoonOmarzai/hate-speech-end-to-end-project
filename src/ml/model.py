import tensorflow
from keras.models import Sequential
from keras.layers import Dense, LSTM, SpatialDropout1D, Embedding
from keras.optimizers import RMSprop

from src.constants import *


class ModelArchitecture:
    def __init__(self):
        pass

    def lstm_model(self):
        # Creating model architecture.
        model = Sequential()
        model.add(Embedding(MAX_WORDS, 100, input_length=MAX_LENGTH))
        model.add(SpatialDropout1D(0.2))
        model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
        model.add(Dense(1, activation='sigmoid'))
        model.summary()

        model.compile(loss='binary_crossentropy',
                      optimizer=RMSprop(),
                      metrics=['accuracy'])

        return model

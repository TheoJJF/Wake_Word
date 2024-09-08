from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, Input, Conv1D, GRU
from tensorflow.keras.layers import LSTM, RNN, Bidirectional, LayerNormalization, BatchNormalization, TimeDistributed
from tensorflow.keras.optimizers import Adam, AdamW
from tensorflow.keras.metrics import Accuracy, Precision, Recall

def model1(input_shape):
    """
    Function creating the model's graph in Keras.

    Argument:
    input_shape -- shape of the model's input data (using Keras conventions)

    Returns:
    model -- Keras model instance
    """

    model = Sequential()
    model.add(Input(shape = input_shape))
    model.add(Conv1D(filters=196, kernel_size=15, strides=4))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.8))

    model.add(GRU(units=128, return_sequences=True))
    model.add(Dropout(0.8))
    model.add(BatchNormalization())

    model.add(GRU(units=128, return_sequences=True))
    model.add(Dropout(0.8))
    model.add(BatchNormalization())
    model.add(Dropout(0.8))

    model.add(TimeDistributed(Dense(1, activation='sigmoid')))

    return model

#
# WORK IN PROGRESS
#
def model2(input_shape):
    """
    Function creating the model's graph in Keras.

    Argument:
    input_shape -- shape of the model's input data (using Keras conventions)

    Returns:
    model -- Keras model instance
    """

    model = Sequential()

    model.add(Input(shape = input_shape))
    model.add(Conv1D(filters=5, kernel_size=3, activation='gelu'))
    model.add(LayerNormalization())

    model.add(Bidirectional(LSTM(units=128,
                                 dropout=0.5,
                                 return_sequences=True)))
    model.add(Bidirectional(LSTM(units=128,
                                 dropout=0.5,
                                 return_sequences=True)))

    model.add(Dense(1, activation='sigmoid'))
    return model
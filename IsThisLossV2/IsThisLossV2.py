# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Code written with inspiration from Eijaz Allibhai at https://towardsdatascience.com/building-a-convolutional-neural-network-cnn-in-keras-329fbbadc5f5
import pandas as pd
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from sklearn.model_selection import train_test_split

###
# Read in, shuffle, preprocess and return a data set.
###
def read_in_data(data_file, validation=False):
    print("Reading in file", data_file)
    df = pd.read_csv(data_file, sep = ",", header = None)
    # df = df.reindex(np.random.permutation(df.index)) # Shuffle the indexes to randomize order
    x = df.iloc[:, 1:].values.astype('float32')
    x /= 255
    x = x.reshape(-1, 100, 100, 1)
    y = df.iloc[:, 0].values
    y = y.reshape(-1, 1)
    y = to_categorical(y)
    return (x, y)

###
# Creates architecture for the CNN model
###
def create_model():
    print("Developing model architecture")
    model = Sequential()
    model.add(Conv2D(64, kernel_size=(5, 5), strides=(1, 1), activation='relu', input_shape=(100, 100, 1)))
    model.add(Flatten())
    model.add(Dense(2, activation='softmax'))
    return model

def getIsThisLossModel():
    x, y = read_in_data("../TrainingDataNCG.csv", validation=True)
    # x_test, y_test = read_in_data("../TestDataNCG.csv")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = create_model()
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=3)
    scores = model.evaluate(x_test, y_test, verbose=0)
    accuracy = scores[1]*100

    save = input("\nWould you like to use the model? (y/n)")
    while save != "y" and save != "n":
        save = input("Not a valid answer.\nWould you like to save the model? (y/n)\n")
    if save == "y":
        return model, accuracy
    else:
        #Try again!
        return getIsThisLossModel()

if __name__ == "__main__":
    getIsThisLossModel()

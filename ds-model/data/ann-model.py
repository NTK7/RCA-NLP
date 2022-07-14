# creating an ANN model to predict the sentiment of a review based on the review text from the data_cleaned.csv file

import pandas as pd
import re
import pickle
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

train_path = 'train.csv'
test_path = 'test.csv'

train_data = pd.read_csv(train_path)
test_data = pd.read_csv(test_path)

# creating an ann model for this
# the model will be trained on the train data
# the model will be tested on the test data


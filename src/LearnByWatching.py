# this part by Boshen Xie
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

# first we need to read from the policy.txt to load data
data = pd.read_table("policy.txt", sep=" ", header=None)
# split the data into train and test
train, test = train_test_split(data, test_size=0.2)

direction_dict = {
    (0, 0): 0,
    (0, 1): 1,
    (1, 0): 2,
    (0, -1): 3,
    (-1, 0): 4,
    (-1, -1): 5,
    (-1, 1): 6,
    (1, -1): 7,
    (1, 1): 8,
}
# for the six cols, combine the first four as the features, the last two combine as the label
# now it is a classification problem
train_x = train.iloc[:, 0:4]
train_y = list(
    zip(train.iloc[:, 4] - train.iloc[:, 2], train.iloc[:, 5] - train.iloc[:, 3])
)
train_y = [direction_dict[i] for i in train_y]
test_x = test.iloc[:, 0:4]
test_y = list(zip(test.iloc[:, 4] - test.iloc[:, 2], test.iloc[:, 5] - test.iloc[:, 3]))
test_y = [direction_dict[i] for i in test_y]

# now we need to train the model
xgbmodel = xgb.XGBClassifier(
    max_depth=5,
    learning_rate=0.1,
    n_estimators=160,
    silent=True,
    objective="multi:softmax",
)
xgbmodel.fit(train_x, train_y)
# now we need to predict the test data
pred = xgbmodel.predict(test_x)
# now we need to calculate the accuracy
accuracy = np.sum(pred == test_y) / len(test_y)
print(accuracy)

# we can see that the accuracy is really promising

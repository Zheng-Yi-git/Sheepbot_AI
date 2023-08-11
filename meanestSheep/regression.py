import numpy as np

# read data from a txt file, with space as the divider
data = np.loadtxt('ex1data1.txt', delimiter=' ')

# the last column is Y, other columns are X. Regress Y on X
X = data[:, :-1]
Y = data[:, -1]

# add a column of 1s to X
X = np.hstack((np.ones((X.shape[0], 1)), X))

class linear_regression:
    def __init__(self, X, y) -> None:
        self.X = X
        self.y = y
        self.beta = None

    def _get_coef(self):
        self.beta = np.linalg.inv(self.X.T.dot(self.X)).dot(self.X.T).dot(self.y)
        return self.beta
    
    def predict(self, X):
        if self.beta == None:
            self._get_coef()
        return X.dot(self.beta)
    



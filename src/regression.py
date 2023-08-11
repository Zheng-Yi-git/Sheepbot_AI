import numpy as np


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


class bot2:
    def __init__(self, train_path, test_path, model=linear_regression) -> None:
        train_data = np.loadtxt(train_path, delimiter=" ")
        X = train_data[:, :-1]
        y = train_data[:, -1]

        X = np.hstack((np.ones((X.shape[0], 1)), X))

        self.lr = model(X, y)

        test_data = np.loadtxt(test_path, delimiter=" ")
        self.X_test = test_data[:, :-1]
        self.y_test = test_data[:, -1]

    def get_mse(self):
        y_pred = self.lr.predict(self.X_test)
        return np.mean((y_pred - self.y_test) ** 2)

    def generate_T(self, data_path, output_path):
        T_data = np.loadtxt(data_path, delimiter=" ")
        X = T_data[:, :-1]
        X = np.hstack((np.ones((X.shape[0], 1)), X))
        # concatenate the predicted y to the X
        y_pred = self.lr.predict(X)
        X = np.hstack((X, y_pred.reshape(-1, 1)))

        np.savetxt(output_path, X, delimiter=" ")

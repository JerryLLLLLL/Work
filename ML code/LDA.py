from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import *

def shuffle_data(X, Y, seed=None):
    if seed:
        np.random.seed(seed)
    idx = np.arange(X.shape[0])
    np.random.shuffle(idx)
    return X[idx], Y[idx]


def normalize(X, axis=-1, p=2):
    lp_norm = np.atleast_1d(np.linalg.norm(X, p, axis))
    lp_norm[lp_norm == 0] = 1
    return X / np.expand_dims(lp_norm, axis)


def standardize(X):
    X_std = np.zeros(len(X))
    X_mean = X.mean(axis=0)
    X_var = X.std(axis=0)

    for i in range(X.shape[1]):
        if X_var[i]:
            X_std[:, i] = (X[:, i] - X_mean[i]) / X_var[i]

    return X_std


def train_test_split(X, y, test_size=0.2, shuffle=False, seed= None):
    if shuffle:
        X_s, y_s = shuffle_data(X, y)

    n_train_sample = int(X.shape[0] * (1-test_size))
    X_train, y_train = X_s[:n_train_sample], y_s[:n_train_sample]
    X_test, y_test = X_s[n_train_sample:], y_s[n_train_sample:]
    return X_train, y_train, X_test, y_test


def accuracy(y, y_pred):
    y = y.reshape(y.shape[0], -1)
    y_pred = y_pred.reshape(y_pred.shape[0], -1)
    return np.sum(y == y_pred)/float(y.shape[0])


def calculate_cov_matrix(X, Y=np.empty((0,0))):
    if not Y.any():
        Y = X
    n_samples = X.shape[0]
    calculate_cov = (1 / (n_samples-1)) * (X - X.mean(axis=0)).T.dot(Y - Y.mean(axis=0))
    return np.array(calculate_cov, dtype=float)


class BiClassLDA():
    def __init__(self):
        self.w = None

    def transform(self, x, y):
        self.fit(x, y)
        x_transform = x.dot(self.w)
        return x_transform

    def fit(self, x, y):
        x = x.reshape(y.shape[0], -1)
        x1 = x[y == 0]
        x2 = x[y == 1]

        S1 = calculate_cov_matrix(x1)
        S2 = calculate_cov_matrix(x2)
        Sw = S1 + S2

        mu1 = x1.mean(axis=0)
        mu2 = x2.mean(axis=0)
        mean_diff = np.atleast_1d(mu1 - mu2)
        mean_diff = mean_diff.reshape(x.shape[1], -1)

        self.w = np.linalg.pinv(Sw).dot(mean_diff)

    def predict(self,X):
        y_predict = []
        for sample in X:
            sample = sample.reshape(1, sample.shape[0])
            h = sample.dot(self.w)
            y = 1 * (h[0][0] < 0)
            y_predict.append(y)
        return y_predict


def main():
    data = datasets.load_iris()
    X = data.data
    Y = data.target

    X = X[Y != 2]
    Y = Y[Y != 2]

    X_train, Y_train, X_test, Y_test = train_test_split(X,Y,test_size=0.33,shuffle=True)

    lda = BiClassLDA()
    lda.fit(X_train,Y_train)
    lda.transform(X_train, Y_train)

    y_pred = lda.predict(X_test)
    y_pred = np.array(y_pred)
    accu = accuracy(Y_test, y_pred)
    print("Accuracy: %10.2f"%accu)


if __name__ == '__main__':
    main()
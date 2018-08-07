from sklearn import datasets
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors
import numpy as np


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
    X_std = np.zeros(X.shape)
    mean = X.mean(axis=0)
    std = X.std()

    for i in range(X.shape[1]):
        if std[i]:
            X_std[:, i] = (X[:, i] - mean[i]) / std

    return X_std


def train_test_split(X, Y, test_size=0.2, shuffle=True, seed=None):
    if shuffle:
        X, Y = shuffle_data(X, Y)

    n_train_sample = int(X.shape[0] * (1-test_size))
    X_train = X[:n_train_sample]; Y_train = Y[:n_train_sample]
    X_test = X[n_train_sample:]; Y_test = Y[n_train_sample:]
    return X_train, X_test, Y_train, Y_test


def accuracy(y, y_pred):
    y = y.reshape(y.shape[0], -1)
    y_pred = y_pred.reshape(y_pred.shape[0], -1)
    return sum(y == y_pred)/float(len(y))


def calculate_cov_matrix(X, Y=np.empty((0,0))):
    if not Y.any():
        Y = X
    n_samples = X.shape[0]
    cov_matrix = 1/(n_samples - 1) * (X - X.mean(axis=0)).T.dot(Y - Y.mean(axis=0))
    return np.array(cov_matrix, dtype=float)


# 计算每列的方差
def calculate_variance(X):
    n_sample = X.shape[0]
    variance = 1 / n_sample * np.diag((X - X.mean(axis=0)).T.dot(X - X.mean(axis=0)))
    return variance


def calculate_std(X):
    return np.sqrt(calculate_variance(X))


def calculate_corr_matrix(X, Y=np.empty([0])):
    cov_matrix = calculate_cov_matrix(X, Y)
    X_std = np.expand_dims(calculate_std(X),1)
    Y_std = np.expand_dims(calculate_std(Y),1)
    corr_matrix = np.divide(cov_matrix, X_std.dot(Y_std.T))
    return np.array(corr_matrix, dtype=float)


class PCA():
    def __init__(self):
        self.eigen_values = None
        self.eigen_vectors = None
        self.k = 2


    def transform(self):

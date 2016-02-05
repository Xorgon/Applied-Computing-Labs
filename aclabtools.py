import pylab as pl
import numpy as np
from scipy.optimize import fsolve


def choose(n, k):
    if 0 <= k <= n:
        p = 1
        for t in range(0, min(k, n - k), 1):
            p = (p * (n - t)) // (t + 1)
        return p
    else:
        return 0


def mls(x, X, y, sigma):
    """ 1D quadratic moving least squares """
    N = max(np.shape(y))
    weights = np.zeros(N)
    A = np.zeros([N, 3])
    A[:, 0] = X**2
    A[:, 1] = X
    A[:, 2] = np.ones([1, N])
    for i in range(1, N):
        weights[i] = np.exp(-np.sum((x - X[i])**2) / (2 * sigma))
    W = np.diag(weights)
    a = np.linalg.lstsq(np.dot(np.dot(A.conj().T, W), A),
                        np.dot(np.dot(A.conj().T, W), y))
    f = a[0][0] * x**2 + a[0][1] * x + a[0][2]
    return f


def mls_error(sigma, X, y):
    """ 1D quadratic moving least squares cross-validation """
    y_test = np.zeros(11)
    error = np.zeros(11)
    for i in range(0, 11):
        y_test[i] = mls(X[i], np.append(X[0: i], X[i+1:-1]),
                        np.append(y[0:i], y[i+1:-1]), sigma)
        error[i] = (y[i]-y_test[i])**2
    sum_error = sum(error)
    return sum_error


def mls_curve_fit(w_array, cd, x):

    # fit moving least squares
    sigma_best = fsolve(mls_error, 0.5, args=(w_array, cd))

    w_fine = np.linspace(0.6, 1.2, 101)
    y_pred = np.zeros(101)
    for i in range(0, 101):
        y_pred[i] = mls(w_fine[i], w_array, cd, sigma_best)
    pl.plot(w_array, cd, 'o', label='XFOIL data')
    pl.plot(w_fine, y_pred, label='MLS fit')
    pl.legend()
    f = mls(x, w_array, cd, sigma_best)
    return f

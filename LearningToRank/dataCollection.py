import numpy as np
from sklearn.tree import DecisionTreeClassifier
import csv
from sklearn.base import clone


def learning(X, y):
    y = np.array(y)
    X = np.array(X)
    X = np.nan_to_num(X)
    # print(X)
    # print(y)
    # # print(X[y==1].shape)
    estimator = DecisionTreeClassifier(max_depth=1)
    T = 10
    zero = np.sum(y == 0)
    one = np.sum(y == 1)
    D = np.repeat(1./(zero*one), zero*one)
    # print(D)
    ys = np.r_[np.zeros(zero*one), np.ones(zero*one)]
    # print(ys)
    nn = np.sum(y == 1)*np.sum(y == 0)
    length = nn*2
    Xs = np.zeros((length, X.shape[1]))
    # print(nn)
    # print(Xs)
    for i, x0 in enumerate(X[y==0]):
        
        for j in range(one):
            Xs[i*one + j] = x0
            # print(x0)
    for i, x1 in enumerate(X[y==1]):
        for j in range(zero):
            Xs[nn + i + one*j] = x1
    h = [None]*T
    a = [0]*T
    e = 1e-6
    # print(Xs)
    for t in range(T):
        Ds = np.r_[D, D]/2
        # print(Xs)
        # print(ys)
        # print(Ds)
        h[t] = clone(estimator).fit(Xs, ys, Ds)
        # print(h[t])
        f_X0 = h[t].predict(X[y == 0])
        f_X1 = h[t].predict(X[y == 1])
        df = np.repeat(f_X0, one) - np.tile(f_X1, zero)

        Wneg = np.sum(D[df == -1])
        Wpos = np.sum(D[df == +1])

        a[t] = 0.5*np.log((Wneg+e)/(Wpos+e))

        D = D*np.exp(a[t]*df)
        D = D/np.sum(D)
    return a, h

def predict(X, a, h):
    X = np.array(X)
    X = np.nan_to_num(X)
    return np.sum([i*j.predict(X) for i, j in zip(a, h)], 0)

X = []
# y = np.array([])
y = []
for i in range(1, 20):
    temp = 'score/' + str(i) + '/score.csv'
    with open(temp, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data = list(row)
            X.append([float(i) for i in data[:-1]])
            # np.append(y, data[-1])
            y.append(float(data[-1]))
# y.astype(int)
# y = [int(float(i)) for i in y]
# print(y)
# print(X)
a, h = learning(X, y)
X = []
for i in range(41,42):
    temp = 'score/' + str(i) + '/score.csv'
    with open(temp, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data = list(row)
            X.append([float(i) for i in data[:-1]])
            # y.append(data[-1])
prediction = predict(X, a, h)
# print(predict(X, a, h))
# print(X)
# print(y)
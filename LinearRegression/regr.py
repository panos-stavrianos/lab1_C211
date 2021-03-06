import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np


def run_command(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    return list(filter(lambda a: a != "", p.decode('utf-8').split("\n")))


files = list(sys.argv)
files.pop(0)
command = "./regr {}".format(" ".join(files))

predictions = []
for r in run_command(command):
    pred = r.split(",")[1].split(" ")
    pred.pop(0)
    predictions.append(list(map(lambda i: i.split("=")[1], pred)))

for index, file_name in enumerate(files):
    with open(file_name, "r") as f:
        data = list(map(lambda line: line.replace("\n", "").split(":"), f.readlines()))
        X = list(map(lambda record: float(record[0]), data))
        Y = list(map(lambda record: float(record[1]), data))
        length = len(X)


    def mse():
        sum_x = sum(X)
        sum_y = sum(Y)
        sum_xy = sum(map(lambda x, y: x * y, X, Y))
        sum_x2 = sum(map(lambda x: x ** 2, X))

        a_d = (length * sum_x2 - sum_x ** 2)
        if round(a_d, 5) == 0.00:
            a = 0
            c = 1
            b = X[0]
            error = 0

            return a, b, c, error

        a = (length * sum_xy - sum_x * sum_y) / a_d
        c = 0

        b = (sum_y - a * sum_x) / length
        error = sum(map(lambda x, y: (y - (a * x + b)) ** 2, X, Y))

        a = round(a, 2)
        b = round(b, 2)
        error = round(error, 2)

        return a, b, c, error


    def get_x_y(a, b, start=-100.0, end=100.0):
        x = np.linspace(start, end, 10)
        y = a * x + b
        return x, y


    fig, ax = plt.subplots()
    _a, _b, _c, _error = mse()

    print(" mse: FILE: {}, a={} b={} c={} err={}".format(file_name,
                                                         _a,
                                                         _b,
                                                         _c,
                                                         _error))
    print("regr: FILE: {}, a={} b={} c={} err={}".format(file_name,
                                                         predictions[index][0],
                                                         predictions[index][1],
                                                         predictions[index][2],
                                                         predictions[index][3]))

    min_X, max_X, min_Y, max_Y = min(X), max(X), min(Y), max(Y)
    if _c == 1:
        min(X)
        y, x = get_x_y(_a, _b, min_Y, max_Y)  # form predicted a,b
    else:
        x, y = get_x_y(_a, _b, min_X, max_X)  # form predicted a,b

    ax.plot(x, y, '-b', label='MSE')

    if _c == 1:
        y, x = get_x_y(float(predictions[index][0]), float(predictions[index][1]), min_Y, max_Y)  # form predicted a,b
    else:
        x, y = get_x_y(float(predictions[index][0]), float(predictions[index][1]), min_X, max_X)  # form predicted a,b

    ax.plot(x, y, '-g', label='regr')

    ax.plot(X, Y, 'ro', label='X,Y')  # the generated X,Y
    ax.legend()
plt.show()

import random

while True:
    files_n = input("How many files do you want to generate:\n")
    if str.isdigit(files_n):
        files_n = int(files_n)
        break
while True:
    prefix = input("Set a prefix(the output file format will be 'prefix_#n'):\n")
    if prefix != "":
        break

for i in range(files_n):
    length = random.randrange(3, 100)
    a = round(random.uniform(-10, 10), 2)
    b = round(random.uniform(-10, 10), 2)
    variance = round(random.uniform(-500, 500), 2)
    constant_x = (random.randrange(-2, 3) < 0, round(random.uniform(-100, 100), 2))

    X = []
    Y = []
    while len(X) <= length:
        if constant_x[0]:
            x_ = constant_x[1]
        else:
            x_ = round(random.uniform(-100, 100), 2)

        # if x_ in X:
        #     continue
        y_ = a * x_ + b + round(random.uniform(-variance, variance), 2)
        y_ = round(y_, 2)
        X.append(x_)
        Y.append(y_)
    with open("{}_{}.csv".format(prefix, i), "w") as f:
        f.writelines(map(lambda x, y: "{}:{}\n".format(x, y), X, Y))

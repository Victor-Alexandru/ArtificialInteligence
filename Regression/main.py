from math import *
from numpy import power
from operator import itemgetter
class Problem:
    def __init__(self, k, noAttributes):
        self.values = []
        self.test = []
        self.k = k
        self.noAttributes = noAttributes
        self.loadData()
        # print(self.test[2][0])

    def __euclideanDistance(self, a, b):
        s = 0.0
        for i in range(len(a)):
            s += (a[i] - b[i]) ** 2
        return sqrt(s)

    def __minkowskiDistance(self, a, b, p):
        s = 0.0
        for i in range(len(a)):
            s += abs((a[i] - b[i])) ** p
        return power(s, 1/p)

    def predict(self):
        predictions = [[] for _ in range(len(self.test))]
        for i in range(len(self.test)):
            neighbors = []
            for j in self.values:
                distance = self.__minkowskiDistance(j[0], self.test[i][0], 5)
                neighbors.append([distance, j[1]])
            for j in range(self.noAttributes):
                s = 0.0
                for l in range(self.k):
                    s += neighbors[l][1][j]
                predictions[i].append(s / self.k)
        errors = []
        for i in range(len(predictions)):
            error = []
            s = []
            for j in range(self.noAttributes):
                s.append([predictions[i][j], self.test[i][1][j]])
                error.append(abs(predictions[i][j] - self.test[i][1][j]))
            errors.append(sum(error))
            message = "Predicted "
            for j in range(self.noAttributes):
                message += str(j + 1) + ".: " + str(s[j][0]) + "(" + str(s[j][1]) + "); "
            message += "\n --> error: " + str(errors[-1])
            print(message)
        return sum(errors) / len(errors)



    def loadData(self):
        f = open("input.txt", "r")
        values = []
        test = []
        line = f.readline()
        indx = 0
        while line != "":
            temp = line.split(",")
            temp = [float(x) for x in temp]
            val = [temp[1:3] + temp[6:], temp[4:6]]
            if indx % 10 == 0:
                test.append(val)
            else:
                values.append(val)
            line = f.readline()
            indx += 1
        self.values = values
        self.test = test


p = Problem(10, 2)
# print("value set of length: ", len(p.values))
# print(p.values)
# print("test set of length: ", len(p.test))
# for t in p.values:
#     print(t)
errors = p.predict()

print()
print(errors)
from network import Network
from matplotlib import pyplot as pp, pylab as pl
def readFromFile(fileName):
    f = open(fileName, "r")
    data = []
    l = f.readline()
    while l != "":
        l = l.split(" ")
        data.append([float(x) for x in l])
        l = f.readline()
    f.close()
    return data


n = Network(21, [6], 3)
data = readFromFile("inputData.txt")
outputData = readFromFile("outputData.txt")
outputData = [int(x[0]) for x in outputData]
n.normalizeData(len(data), len(data[1]), data)
errorsList = n.learn(data, outputData, 300)
x = [x for x in range(len(errorsList))]
pp.plot(x, errorsList, 'k')
pl.show()
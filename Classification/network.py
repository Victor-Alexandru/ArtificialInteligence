from layer import Layer
from math import exp, sqrt

LEARNING_RATE = 0.01
NO_LABELS = 3


class Network:
    def __init__(self, noInputs, hiddens, noOutputs):
        self.__noInputs = noInputs
        self.__noOutputs = noOutputs
        self.__noHL = len(hiddens)
        layers = [Layer(noInputs, 1)]  # input layer
        layers += [Layer(hiddens[0], noInputs)]  # first hidden layer
        for i in range(1, self.__noHL):  # additional hidden layers
            layers.append(Layer(hiddens[i], hiddens[i - 1]))
        layers.append(Layer(noOutputs, hiddens[-1]))  # output layer
        self.__layers = layers

    def activate(self, input):
        for i in range(self.__noInputs):
            self.__layers[0].neurons[i].output = input[i]
        for l in range(1, self.__noHL + 2):
            for n in self.__layers[l].neurons:
                info = [self.__layers[l - 1].neurons[i].output for i in range(self.__layers[l - 1].noNeurons)]
                n.activate(info)

    def backPropagate(self, error):
        for l in range(self.__noHL + 1, 0, -1):
            i = 0
            for n1 in self.__layers[l].neurons:
                if l == self.__noHL + 1:
                    n1.setErrorLin(-n1.output + error[i])
                else:
                    sumError = 0.0
                    for n2 in self.__layers[l + 1].neurons:
                        sumError += n2.weights[i] * n2.error
                    n1.setErrorSig(sumError)
                for j in range(len(n1.weights)):
                    netWeight = n1.weights[j] + LEARNING_RATE * n1.error * self.__layers[l - 1].neurons[j].output
                    n1.setWeight(j, netWeight)
                i += 1

    def errorComputeClass(self, target, noLabels):
        aux = [n.output for n in self.__layers[self.__noHL + 1].neurons]
        m = max(aux)
        aux = [exp(x - m) for x in aux]
        s = sum(aux)
        transfOutput = [x / s for x in aux]
        m = transfOutput[0]
        computeLabel = 1
        for i in range(noLabels):
            if transfOutput[i] > m:
                m = transfOutput[i]
                computeLabel = i + 1
        if target == computeLabel:
            return 0
        else:
            return 1

    def checkGlobalError(self, error):
        errors = sum(error)
        error = errors / len(error)
        if error < 0.05:
            return True
        return False

    def learn(self, inData, outData, epochLimit):
        stop = False
        epoch = 0
        errors = []
        while not stop and epoch < epochLimit:
            globalError = []
            for d in range(len(inData)):
                self.activate(inData[d])
                err = [0 for _ in range(self.__noOutputs)]
                err[outData[d] - 1] = 1
                globalError.append(self.errorComputeClass(outData[d], NO_LABELS))
                self.backPropagate(err)
            errors += [sum(globalError)]
            epoch += 1
        return errors

    def getLayers(self):
        return self.__layers

    def normalizeData(self, n, noLabels, data):
        for j in range(noLabels):
            summ = 0.0
            for i in range(n):
                summ += data[i][j]
            mean = summ / n
            squareSum = 0.0
            for i in range(n):
                squareSum += (data[i][j] - mean) ** 2
            deviation = sqrt(squareSum / n)
            for i in range(n):
                data[i][j] = (data[i][j] - mean) / deviation

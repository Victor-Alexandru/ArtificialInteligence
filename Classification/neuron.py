from math import exp
from random import random
class Neuron:
    def __init__(self, noInputs):
        self.noInputs = noInputs
        self.weights = [random() * 2 - 1 for _ in range(noInputs)]
        self.output = 0.0
        self.error = 0.0

    def activate(self, info):
        s = 0
        for i in range(self.noInputs):
            s += info[i] * self.weights[i]
        self.output = 1 / (1.0 + exp(-s))

    def setErrorSig(self, value):
        self.error = self.output * (1.0 - self.output) * value

    def setWeight(self, i, value):
        self.weights[i] = value

    def setErrorLin(self, value):
        self.error = value

    def __str__(self):
        weights = [round(x, 4) for x in self.weights]
        return str(weights) + "out: " + str(round(self.output,4))
from neuron import Neuron


class Layer:
    def __init__(self, noNeurons, noInputs):
        self.noNeurons = noNeurons
        self.__noInputs = noInputs
        self.neurons = [Neuron(noInputs) for _ in range(noNeurons)]

    def __str__(self):
        return "Layer with " + str(self.noNeurons) + " neurons and " + str(self.__noInputs) + " input neurons"
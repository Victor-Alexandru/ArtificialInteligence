import random
import itertools
from statistics import mean, stdev
from operator import itemgetter


class Ant:
    def __init__(self, start):
        self._solution = list()
        self._solution.append(start)

        self._fitness = -1

    def __repr__(self):
        return str(self._solution) + " - " + str(self._fitness)

    def _computeFitness(self):
        self._fitness = 0

    def fitness(self):
        if self._fitness == -1:
            self._computeFitness()
        return self._fitness

    def move(self, cube):
        self._solution.append(cube)

    def getLast(self):
        return self._solution[-1]

    def getLastButOne(self):
        return self._solution[len(self._solution) - 2]

    def getSolution(self):
        return self._solution.copy()


PROBLEM_LENGTH = 10


class Controller:
    _PH_GLOBAL_DEGRADATION = 0.3
    _PH_LOCAL_DEGRADATION = 0.4

    _INITIAL_PH_TRAIL = 1
    _LOCAL_QUANTITY = _INITIAL_PH_TRAIL

    _MAX_NR_OF_ITERATIONS = 10
    _PRINT_EVERY_ITERATIONS = 1

    _EXPLOITATION_CHANCE = 1
    _ALPHA = 1
    _BETA = 1

    def __init__(self):
        self._NR_OF_ANTS = 20
        self._MAX_FITNESS = 10

        self._NR_OF_STEPS_TO_BUILD_SOLUTION = 10 * 2 - 1

        self._colony = list()
        self._cost = list()
        self._trace = list()

        self._solution = None

        self._initCost()
        self._initTrace()
        self._generateColony()
        pr = Problem("input.txt")
        self._cub_list = pr.loadData()

    def _initCost(self):
        self._buildMatrix(self._cost, 0)
        for i in range(PROBLEM_LENGTH):
            for j in range(i + 1, PROBLEM_LENGTH):
                self._cost[i][j] = self._cost[j][i] = \
                    self.cubeIntersection(self._cub_list[i], self._cub_list[j])

    def _buildMatrix(self, matrix, defaultValue):
        for i in range(PROBLEM_LENGTH):
            matrix.append(list())
            for j in range(PROBLEM_LENGTH):
                matrix[i].append(defaultValue)

    def cubeIntersection(self, first_List, Second_List):
        possibleIntersections = 1
        for i in first_List:
            for j in Second_List:
                if i == j:
                    possibleIntersections += 1
        return possibleIntersections

    def _initTrace(self):
        self._buildMatrix(self._trace, self._INITIAL_PH_TRAIL)

    def _generateColony(self):
        for i in range(self._NR_OF_ANTS):
            self._colony.append(Ant(random.randint(0, PROBLEM_LENGTH - 1)))

    def runAlg(self):
        for i in range(self._MAX_NR_OF_ITERATIONS):
            self._iteration()
            self._statistics(i)
            if self._solution is not None:
                break
            self._resetColony()

        if self._solution is not None:
            print(self._solution)
        else:
            print("Sorry, no solution found this time!")

    def _statistics(self, iterationNr):
        if iterationNr % self._PRINT_EVERY_ITERATIONS != 0:
            return
        print("Iteration: " + str(iterationNr), end="\n\n")
        for ant in self._colony:
            print(ant)
        print('------------------------')

    def _iteration(self):
        for i in range(self._NR_OF_STEPS_TO_BUILD_SOLUTION):
            for ant in self._colony:
                wordPosChosen = self._chooseNextMove(ant)
                ant.move(wordPosChosen[0])
                try:
                    self._updatePheromoneEdge(ant.getLast(), ant.getLastButOne(),
                                              self._PH_LOCAL_DEGRADATION, self._LOCAL_QUANTITY)
                except TypeError:
                    print(ant)

        bestAnt = max(self._colony, key=lambda x: x.fitness())

        if bestAnt.fitness() == 9:
            self._solution = bestAnt.getSolution()
        else:
            self._updateGlobalPheromones(bestAnt)

    def _chooseNextMove(self, ant):
        if random.randint(0, 100) <= self._EXPLOITATION_CHANCE:
            return self._exploit(ant), 0
        else:
            return self._explore(ant), 1

    def _exploit(self, ant):
        values = list()
        for i in range(PROBLEM_LENGTH):
            if i not in ant.getSolution():
                x = self._computeProductCostTrace(ant.getLast(), i)
                values.append((i, x))
        wordPosChosen = max(values, key=itemgetter(1))
        return wordPosChosen[0]

    def _computeProductCostTrace(self, i, j):
        return pow(1 / self._cost[i][j], self._ALPHA) * pow(self._trace[i][j], self._BETA)

    def _explore(self, ant):
        probabilities = self._computeAllProbabilities(ant)
        cumulativeSum = self._computeCumulativeSum(probabilities)
        random1 = random.randint(1, 100) / 100

        for i in range(len(cumulativeSum) - 1):
            if cumulativeSum[i] >= random1 > cumulativeSum[i + 1]:
                return i

    def _computeAllProbabilities(self, ant):
        probabilities = list()
        sumOfAllProducts = 0

        for i in range(len(Problem.WORDS)):
            if i not in ant.getSolution():
                sumOfAllProducts += self._computeProductCostTrace(i, ant.getLast())

        for i in range(len(Problem.WORDS)):
            if i not in ant.getSolution():
                probabilities.append(self._computeProductCostTrace(i, ant.getLast()) / sumOfAllProducts)
            else:
                probabilities.append(0)
        return probabilities

    def _computeCumulativeSum(self, probabilities):
        cumulativeSum = [1]
        for i in range(1, len(probabilities)):
            cumulativeSum.append(sum(probabilities[i:]))
        cumulativeSum.append(0)
        return cumulativeSum

    def _updatePheromones(self, ant, degradation, quantity):
        solution = ant.getSolution()
        for i in range(len(solution) - 1):
            self._updatePheromoneEdge(solution[i], solution[i + 1], degradation, quantity)
        self._updatePheromoneEdge(solution[-1], solution[0], self._PH_LOCAL_DEGRADATION, self._LOCAL_QUANTITY)

    def _updatePheromoneEdge(self, i, j, degradation, quantity):
        self._trace[i][j] = self._trace[j][i] = (1 - degradation) * self._trace[i][j] + quantity * degradation

    def _updateGlobalPheromones(self, bestAnt):
        solution = bestAnt.getSolution()
        bestEdges = [(solution[-1], solution[0])]
        for i in range(len(solution) - 1):
            bestEdges.append((solution[i], solution[i + 1]))

        for i in range(len(Problem.WORDS)):
            for j in range(i + 1, len(Problem.WORDS)):
                quantity = 1 / (self._MAX_FITNESS - bestAnt.fitness()) if (i, j) in bestEdges else 0
                self._updatePheromoneEdge(i, j, self._PH_GLOBAL_DEGRADATION, quantity)

    def _resetColony(self):
        for i in range(self._NR_OF_ANTS):
            self._colony[i] = Ant(self._colony[i].getLast())


class Population:
    def __init__(self, list_of_individs):
        self.list_of_individs = list_of_individs

    def get_length(self):
        return len(self.list_of_individs)

    def get_population(self):
        return self.list_of_individs

    # adding a pyramid
    def add_individ(self, individ):
        self.list_of_individs.append(individ)

    # evaluate the population
    def evaluate(self):
        print("The average fitness is : ", mean([x.fitness() for x in self.list_of_individs]))
        print("The standart deviation  is : ", stdev([x.fitness() for x in self.list_of_individs]))

        return max(self.list_of_individs, key=lambda x: x.fitness())

    def get_best_fitness(self):
        return max(self.list_of_individs, key=lambda x: x.fitness())


class Problem:
    # specific data for the problem
    def __init__(self, file):
        self.file = file

    def loadData(self):
        all_pyramids = []
        with open(self.file, "r") as f:
            for line in f:
                line = line.split(",")
                line[-1] = line[-1][0]
                for i in range(0, len(line) - 1, 2):
                    all_pyramids.append([int(line[i]), line[i + 1]])

        return all_pyramids


c = Controller()
c._buildMatrix(list(), 0)

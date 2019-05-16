import random
import itertools
from statistics import mean, stdev
import matplotlib.pyplot as plt

''''
here we code the piramid
'''

CONST_ALL_COLLORS = ['r', 'g', 'a']


class Individ:
    def __init__(self, size, cub_list):
        self._cub_list = list(cub_list)
        self.size = self.fitness()

    def get_pyramid(self):
        return self._cub_list

    def fitness(self):
        """"
        we choose the pyramid based on the highest level of
        the construction (how high is the piramid)-actually the size of the piramid
        """
        fit = 1
        for i in range(0, len(self._cub_list) - 1):
            if self._cub_list[i][0] > self._cub_list[i + 1][0] and self._cub_list[i][1] != self._cub_list[i + 1][1]:
                fit += 1
            else:
                break
        return fit

    def swap_mutate(self, prob):
        '''
        Randomly choose 2 genes and swap their values
        2 cubes
        '''

        if prob < random.random():
            return False
        # getting the min and the max values
        i1 = random.randint(0, len(self._cub_list) - 1)
        i2 = random.randint(0, len(self._cub_list) - 1)
        if (i1 != i2):
            self._cub_list[i1], self._cub_list[i2] = self._cub_list[i2], self._cub_list[i1]
        else:
            return False

        return True

    def order_crossover(self, other_pyramid, prob):
        ''''
        crossover between the self pyramid and other pyramid
        depending on the probability
        we combine a part of a pyramid with a part of the other pyramid
        '''
        if prob < random.random():
            return False, False
        child = []
        t = random.randint(0, len(self._cub_list) - 1)
        child = self._cub_list[:t] + other_pyramid.get_pyramid()[t:]

        return True, Individ(len(child), child[::-1])

    def __str__(self):
        pString = ""
        for cub in self._cub_list:
            for i in range(cub[0]):
                pString += cub[1] + " "
            pString += "\n"

        return pString[::-1]

    def __repr__(self):
        return str(self.fitness())


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

    def return_population(self):
        rez = list(itertools.permutations(self.loadData()))[:40]
        for i in range(0, len(rez)):
            rez[i] = Individ(len(list(rez[i])), rez[i])
        return Population(rez)

    def loadData(self):
        all_pyramids = []
        with open(self.file, "r") as f:
            for line in f:
                line = line.split(",")
                line[-1] = line[-1][0]
                for i in range(0, len(line) - 1, 2):
                    all_pyramids.append([int(line[i]), line[i + 1]])

        return all_pyramids


class Algorithm:
    def __init__(self, problem):
        self._population = problem.return_population()

    def iteration(self, index, prob):
        '''
        an iteration
        prob: the probability the mutation to occure
        '''

        pop_list = self._population.get_population()
        # recombination selection
        i1 = random.randint(0, self._population.get_length() - 1)
        i2 = random.randint(0, self._population.get_length() - 1)

        if (i1 != i2):
            created, c = pop_list[i1].order_crossover(pop_list[i2], prob)
            if created:
                mutated = c.swap_mutate(prob)
                if mutated:
                    f1 = pop_list[i1].fitness()
                    f2 = pop_list[i2].fitness()

                    '''
                    the repeated evaluation of the parents can be avoided
                    if  next to the values stored in the individuals we
                    keep also their fitnesses
                    '''
                    fc = c.fitness()
                    if (f1 < fc):
                        pop_list[i1] = c
                    elif (f2 < fc):
                        pop_list[i2] = c
        print(index, pop_list)

    def run(self, nrIteration, prob):
        for i in range(nrIteration):
            self.iteration(i, prob)

        self.statistics()

    def statistics(self):
        self._population.evaluate()

    def get_best_individ(self):
        return self._population.get_best_fitness()


def main_function():
    p = Problem('input.txt')
    alg = Algorithm(p)
    probability = 1
    alg.run(nrIteration=1000, prob=probability)


# b
def main_functionTwo():
    all_biggest_fitness = []
    for i in range(30):
        p = Problem('input.txt')
        alg = Algorithm(p)
        probability = 1
        alg.run(nrIteration=1000, prob=probability)
        all_biggest_fitness.append(alg.get_best_individ())

    print("The average fitness for 30 runs  is : ", mean([x.fitness() for x in  all_biggest_fitness]))
    print("The standart deviation  for 30 runst is : ", stdev([x.fitness() for x in  all_biggest_fitness]))
    x = [i for i in range(30)]
    y = [i.fitness() for i in all_biggest_fitness]
    plt.plot(x, y)
    plt.show()


# pct a
# main_function()
main_functionTwo()
# pct b


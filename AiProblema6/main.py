import random

''''
here we code the piramid
'''

CONST_ALL_COLLORS = ['r', 'g', 'a']


class Individ:
    def __init__(self, size, cub_list):
        self.size = len(cub_list)
        self._cub_list = cub_list

    def get_pyramid(self):
        return self._cub_list

    def fitness(self):
        """"
        we choose the pyramid based on the highest level of
        the construction (how high is the piramid)-actually the size of the piramid
        """
        return len(self._cub_list)

    def mutate(self, prob):
        '''
        Performs a mutation on an individual,with the probability prob
        an individual cube will be added on the pyramid at a random position,
        between the base and the root
        '''

        if prob < random.random():
            return False
        # getting the min and the max values
        base_length = self._cub_list[0][0]
        root_length = self._cub_list[-1][0]
        # checking if the cub with length 1 (the root) exists in the pyramid
        root_length = 2 if root_length <= 1 else root_length
        cub_dimension = [x[0] for x in self._cub_list]
        cub_colors = [x[1] for x in self._cub_list]
        # generating a random number that is between root and base and not in our cub dimension
        new_length = base_length
        while new_length in cub_dimension:
            new_length = random.randint(root_length - 1, base_length + 1)
        # putting the cube in the pyramid (getting the position)
        position = 0
        for cube in self._cub_list:
            if new_length > cube[0]:
                break
            position += 1

        # determine dynamically the color
        if position == len(self._cub_list):
            new_color = self._cub_list[position - 1][1]
            while new_color == self._cub_list[position - 1][1]:
                new_color = cub_colors[random.randint(0, len(cub_colors) - 1)]
        elif position == 0:
            new_color = self._cub_list[0][1]
            while new_color == self._cub_list[0][1]:
                new_color = cub_colors[random.randint(0, len(cub_colors) - 1)]
        else:
            new_color = self._cub_list[position][1]
            while new_color == self._cub_list[position - 1][1] or new_color == self._cub_list[position][1]:
                new_color = CONST_ALL_COLLORS[random.randint(0, len(CONST_ALL_COLLORS) - 1)]

        new_cube = [new_length, new_color]

        # inserting the cube in the pyramid
        self._cub_list.insert(position, new_cube)
        return True

    def crossover(self, other_pyramid, prob):
        ''''
        crossover between the self pyramid and other pyramid
        depending on the probability
        we can say that we merge 2 pyramids if they have different dimensions
        return a pyramid child
        '''
        if prob < random.random():
            return False, False
        child = []
        # getting the sizes list
        sizes = [x[0] for x in self.get_pyramid()] + [y[0] for y in other_pyramid.get_pyramid()]
        sizes = set(sizes)  # making the sizes unig
        # getting the colors list
        colors = [x[1] for x in self.get_pyramid()] + [y[1] for y in other_pyramid.get_pyramid()]
        colors = list(set(colors))  # making the sizes unig
        # creating the child,pyramid
        sizes = sorted(list(sizes), key=lambda x: x)

        first_cube = [sizes.pop(0), colors[0]]
        child.append(first_cube)
        for cub_size in sizes:
            last_color = child[-1][1]
            generated_color = child[-1][1]
            while generated_color == last_color:
                generated_color = random.choice(list(colors))

            child.append([cub_size, generated_color])

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
        get_selected = self.selection()
        individ = min(self.list_of_individs, key=lambda x: x.size)
        return [get_selected, individ]

    def selection(self):
        """"
        we choose survival selection ,based on the fitnees

        """
        return sorted(self.list_of_individs, key=lambda x: x.size)[-3:]


class Problem:
    # specific data for the problem
    def __init__(self, file):
        self.file = file

    def return_population(self):
        p = Population([])
        [p.add_individ(Individ(len(x), x)) for x in self.loadData()]
        return p

    def loadData(self):
        all_pyramids = []
        with open(self.file, "r") as f:
            for line in f:
                line = line.split(",")
                line[-1] = line[-1][0]
                pyramid = []
                for i in range(0, len(line) - 1, 2):
                    pyramid.append([int(line[i]), line[i + 1]])
                all_pyramids.append(pyramid)
        return all_pyramids


class Algorithm:
    def __init__(self, problem):
        self._population = problem.return_population()

    def iteration(self, prob):
        '''
        an iteration
        prob: the probability the mutation to occure
        '''
        pop_list = self._population.get_population()
        i1 = random.randint(0, self._population.get_length() - 1)
        i2 = random.randint(0, self._population.get_length() - 1)

        if (i1 != i2):

            created, c = pop_list[i1].crossover(pop_list[i2], prob)
            if created:
                mutated = c.mutate(prob)
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
        print(pop_list)
    def run(self, nrIteration, prob):
        for i in range(nrIteration):
            self.iteration(prob)

        self.statistics()

    def statistics(self):
        print(self._population.evaluate())
        for individ in self._population.evaluate():
            print(individ)


def main_function():
    p = Problem('input.txt')
    alg = Algorithm(p)
    probability = 1
    alg.run(nrIteration=500, prob=probability)


main_function()

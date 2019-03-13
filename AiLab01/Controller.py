from Problem import  Problem
class Controller:
    def __init__(self, problem):
        self.__problem = problem

    def BFS(self, root):

        q = [root]

        while len(q) > 0:
            currentState = q.pop(0)

            if currentState.getValues()[-1] == self.__problem.getFinal():
                return currentState
            q = q + self.__problem.expand(currentState)

    def BestFS(self, root):

        visited = []
        toVisit = [root]
        while len(toVisit) > 0:
            node = toVisit.pop(0)
            visited = visited + [node]
            if node.getValues()[-1] == self.__problem.getFinal():
                return node
            aux = []
            for x in self.__problem.expand(node):
                if x not in visited:
                    aux.append(x)
            aux = [[x, self.__problem.heuristics(x, self.__problem.getFinal())] for x in aux]
            aux.sort(key=lambda x: x[1])
            aux = [x[0] for x in aux]
            toVisit = aux[:] + toVisit


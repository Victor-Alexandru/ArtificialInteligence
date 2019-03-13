from State import State


class Problem:
    def __init__(self, initial, final):
        self.__initialConfig = initial
        self.__finalConfig = final
        self.__initialState = State()
        self.__initialState.setValues([self.__initialConfig])

    def expand(self, currentState):
        myList = []
        currentConfig = currentState.getValues()[-1]
        for j in range(currentConfig.getSize()):
            for x in currentConfig.nextConfig(j):
                myList.append(currentState + x)

        return myList

    def getFinal(self):
        return self.__finalConfig

    def getRoot(self):
        return self.__initialState

    def heuristics(self, state, finalC):
        """
        we will rank the points based on the how many restrictions did they have

        """
        l = finalC.getSize()
        count = 2 * l
        for i in range(l):
            if state.getValues()[-1].getValues()[i] != finalC.getValues()[i]:
                count = count - 1
        return count

    def readFromFile(self):
        #aici trebuie sa citesti sudoku
        pass
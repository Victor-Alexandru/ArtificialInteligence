from Configuration import Configuration


class State:
    '''
    @author Victor Viena98
    holds a PATH of configurations
    '''

    def __init__(self):
        self.__values = []

    def setValues(self, values):
        self.__values = values[:]

    def getValues(self):
        return self.__values[:]

    def __str__(self):

        pString = ""
        for row_list in self.getValues():
            s = ''
            [s + str(x) + " " for x in row_list]
            pString += s + "\n"
        return pString

    def __add__(self, something):
        aux = State()
        if isinstance(something, State):
            aux.setValues(self.__values + something.getValues())
        elif isinstance(something, Configuration):
            aux.setValues(self.__values + [something])
        else:
            aux.setValues(self.__values)
        return aux

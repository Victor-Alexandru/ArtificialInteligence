class Configuration:
    '''
    holds a configurations of frogs
    '''

    def __init__(self, positions):
        self.__size = len(positions) #here is the n
        self.__values = positions[:]

    def getSize(self):
        return self.__size

    def getValues(self):
        return self.__values[:]

    def nextConfig(self, nr, row, col):
        """
        here we put an number in the coresponded place
        :param nr,row,col:
        :return void:
        """
        try:
            if row > self.getSize() or col > self.getSize():
                raise ValueError("Invalid indexes")

            if self.__values[row][col] == -1:
                self.__values[row][col] = nr
            else:
                raise ValueError("Invalid box")


        except ValueError as e:
            print(e)

    def __eq__(self, other):
        if not isinstance(other, Configuration):
            return False
        if self.__size != other.getSize():
            return False
        for i in range(self.__size):
            if self.__values[i] != other.getValues()[i]:
                return False
        return True

    def __str__(self):
        return str(self.__values)

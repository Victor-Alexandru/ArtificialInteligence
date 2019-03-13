from  Controller import Controller
from Configuration import Configuration
from Problem import Problem


class Ui:
    def __init__(self):
        self.__iniC = Configuration([[3, -1, -1, 2], [-1, 1, 4, -1], [1, 2, -1, 4], [-1, 3, 2, 1]])
        self.__finC = Configuration([[3, 4, 1, 2], [2, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])
        self.__p = Problem(self.__iniC, self.__finC)
        self.__contr = Controller(self.__p)

    def printMainMenu(self):
        s = ''
        s += "[[3, -1, -1, 2], [-1, 1, 4, -1], [1, 2, -1, 4], [-1, 3, 2, 1]] and [[3, 4, 1, 2], [2, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]] are the default initial and final config.\n"
        s += "0 - exit \n"
        s += "2 - find a path with BFS \n"
        s += "3 - find a path with GBFS\n"
        print(s)

    def findPathBFS(self):
        print("BFS needed")
        # startClock = time()
        # print(str(self.__contr.BFS(self.__p.getRoot())))
        # print('execution time = ', time() - startClock, " seconds")

    def findPathGBFS(self):
        print("GBFS needed")
        # startClock = time()
        # print(str(self.__contr.BestFS(self.__p.getRoot())))
        # print('execution time = ', time() - startClock, " seconds")

    def run(self):
        runM = True
        self.printMainMenu()
        while runM:
            try:
                command = int(input(">>"))
                if command == 0:
                    runM = False
                elif command == 2:
                    self.findPathBFS()
                elif command == 3:

                    self.findPathGBFS()
            except:
                print('invalid command')

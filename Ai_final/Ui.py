from Controller import SudokuController
from Sudoku import Sudoku
from time import time


class UI:
    def __init__(self):
        s = Sudoku()
        self._c = SudokuController(s)

    def printMainMenu(self):
        s = ''
        s += "Look in the file to see the configuration you choose.\n"
        s += "0 - exit \n"
        s += "2 - find a path with BFS \n"
        s += "3 - find a path with GBFS\n"
        print(s)

    def findPathBFS(self):
        startClock = time()
        [print(x) for x in self._c.bfs()]
        print('execution time = ', time() - startClock, " seconds")

    def findGBF(self):
        startClock = time()
        [print(x) for x in self._c.gbfs()]
        print('execution time = ', time() - startClock, " seconds")

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
                    self.findGBF()
            except ValueError as e:
                print(e)
                print('invalid command')

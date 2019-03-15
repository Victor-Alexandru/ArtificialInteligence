from math import sqrt
import ipdb
from operator import itemgetter

def checkdups(slist):
    fr =[]
    for i in range(100):
        fr.append(0)

    for elem in slist:
        if elem !=-1:
            fr[elem]+=1

    for freq in fr:
        if freq ==2:
            return  True

    return False



class Sudoku:
    """
    @powerd by Victor Viena

    """

    def __init__(self):
        self._table = self.read_from_file()
        self._table_size = int(len(self._table))

    def check_part(self):
        """
        checks if the sudoku is partialy correct
        """
        #check rows
        for row in self._table:
            if checkdups(row) is True:
                return  False
        #check cols
        cols =[]
        for  i in range(0,len(self._table)):
            cur_col = []
            for j in range(0, len(self._table)):
                cur_col.append(self._table[j][i])
            if checkdups(cur_col) is True:
                return  False
        return  True


    def read_from_file(self):
        """
        we return the array that we read from the file
        :return:
        """
        rez = []
        with open("input.txt", "r") as file:
            for line in file:
                line = line.split()
                a = [int(x) for x in line]
                rez.append(a)

        return rez

    def get_table_size(self):
        return self._table_size

    def get_table(self):
        return self._table

    def first_free_position(self):
        """
        getting the indexes of the next free position in the table
        """

        for row in self._table:
            for col in row:
                if col == -1:
                    return self._table.index(row), row.index(col)
        return [0, 0]

    def get_all_free(self):
        """
        this will return a list with all free position indexes
        """
        rez = []
        for row in range(0, len(self._table)):
            for col in range(0, len(self._table)):
                if self._table[row][col] == -1:
                    rez.append([row, col])

        return rez

    def chek_row(self, row, number):
        """
        check if a number is used in a row
        """
        flag = False
        for value in self._table[row]:
            flag = True if number == value else False

        return flag

    def check_col(self, col, value):
        """
        check if a number is used in a col
        """
        flag = False
        for row in self._table:
            flag = True if value == row[col] else False
        return flag

    def check_square(self, row, col, value):
        """
        check if an element is used in a square
        """

        square_side = int(sqrt(self.get_table_size()))
        start_index = 0

        is_down = True if row < square_side else False
        is_left = True if col < square_side else False

        if is_left == is_down:
            params = [0, 0] if (is_down and is_left) else [square_side, square_side]
        else:
            params = [0, square_side] if (is_down and not (is_left)) else [square_side, 0]

        # first the horizontal table
        flag = False
        for row in range(params[0], params[0] + square_side):
            for col in range(params[1], params[1] + square_side):
                flag = True if self.get_table()[row][col] == value else False

        return flag

    def is_safe(self, row, col, value):
        """
        see if we can place the  value
        """
        if self.check_col(col, value) is True:
            return False
        if self.chek_row(row, value) is True:
            return False
        if self.check_square(row, col, value) is True:
            return False

        return True

    def __eq__(self, other):

        if not (isinstance(other, Sudoku)):
            return False
        if self.get_table_size() != other.get_table_size():
            return False
        for i in range(self.get_table_size()):
            for j in range(self.get_table_size()):
                if self._table[i][j] != other.get_table()[i][j]:
                    return False
        return True

    def calculate_point_heuristic(self, row, col, value):
        """
        calculate the heuristic in function of HOW MANY RESTRICTIONS DID THEY HAVE
        """
        diff_list = []
        # diferent items per colum
        for lrow in self._table:
            if value != lrow[col] and (lrow[col] not in diff_list):
                diff_list.append(lrow[col])

        # different items per ROOW


        for number in self._table[row]:
            if number != value and (number not in diff_list):
                diff_list.append(number)

        # DIFFERENT ITEMS PER SQUARE
        square_side = int(sqrt(self.get_table_size()))

        is_down = True if row < square_side else False
        is_left = True if col < square_side else False

        if is_left == is_down:
            params = [0, 0] if (is_down and is_left) else [square_side, square_side]
        else:
            params = [0, square_side] if (is_down and not (is_left)) else [square_side, 0]

        for row in range(params[0], params[0] + square_side):
            for col in range(params[1], params[1] + square_side):
                if self.get_table()[row][col] != value and (self.get_table()[row][col] not in diff_list):
                    diff_list.append(self.get_table()[row][col])

        return len(diff_list)

    def first_heuristics_pos(self):
        if len(self.return_best_heuristic_positions()) != 0:
            return self.return_best_heuristic_positions()[0][1]
        else:
            return  self.first_free_position()
    def return_best_heuristic_positions(self):
        """
        :return the sorted list with possible candidates
        """
        possible_points = self.get_all_free()
        rez = []
        for point in possible_points:
            rez.append([self.calculate_point_heuristic(point[0], point[1], self._table[point[0]][point[1]]), point])

        rez = sorted(rez, key=itemgetter(0))

        return rez[::-1]

    def __lt__(self, other):
        return self.heuristics() < other.heuristics()

    def __str__(self):
        pString = ""
        for row in self._table:
            for col in row:
                pString += str(col) + " "
            pString += "\n"
        return pString


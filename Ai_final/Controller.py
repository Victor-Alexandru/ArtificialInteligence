from copy import deepcopy
from Sudoku import Sudoku


class SudokuController:
    def __init__(self, s_table):
        self._s_table = s_table

    def get_s_table(self):
        return self._s_table

    @staticmethod
    def final_state(board):
        return board.first_free_position() == [0, 0]

    @staticmethod
    def expand(s_table):

        row, col = s_table.first_free_position()
        table_len = s_table.get_table_size()
        partial_calculate = []

        for number in range(1, table_len + 1):
            if s_table.is_safe(row, col, number):
                new_table = deepcopy(s_table)
                new_table.get_table()[row][col] = number
                partial_calculate.append(new_table)
        return partial_calculate

    @staticmethod
    def greedy_expand(s_table):
        row, col = s_table.first_heuristics_pos()

        table_len = s_table.get_table_size()
        partial_calculate = []
        print(row, col)
        for number in range(1, table_len + 1):
            if s_table.is_safe(row, col, number):
                new_table = deepcopy(s_table)
                new_table.get_table()[row][col] = number
                partial_calculate.append(new_table)
        return partial_calculate

    def bfs(self):
        visited = [self._s_table]
        queue = [[self._s_table]]
        while len(queue) > 0:
            partial_result = queue.pop(0)
            if self.final_state(partial_result[-1]):
                return partial_result
            for table in self.expand(partial_result[-1]):
                if table not in visited:
                    partial_result += [table]
                    visited.append(partial_result[-1])
                queue.append(partial_result)
                partial_result = partial_result[:-1]
        return None

    def gbfs(self):
        visited = [self._s_table]
        queue = [[self._s_table]]
        while len(queue) > 0:
            partial_result = queue.pop(0)
            if self.final_state(partial_result[-1]):
                return partial_result
            for table in self.greedy_expand(partial_result[-1]):
                if table not in visited:
                    partial_result += [table]
                    visited.append(partial_result[-1])
                queue.append(partial_result)
                partial_result = partial_result[:-1]
        return None

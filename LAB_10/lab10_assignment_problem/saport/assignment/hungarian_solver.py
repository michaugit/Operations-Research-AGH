import numpy as np
from .model import Assignment, AssignmentProblem, NormalizedAssignmentProblem
from typing import List, Dict, Tuple, Set

class Solver:
    '''
    A hungarian solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    extract_mins(costs: np.Array):
        substracts from columns and rows in the matrix to create 0s in the matrix
    find_max_assignment(costs: np.Array) -> Dict[int,int]:
        finds the biggest possible assinments given 0s in the cost matrix
        result is a dictionary, where index is a worker index, value is the task index
    add_zero_by_crossing_out(costs: np.Array, partial_assignment: Dict[int,int])
        creates another zero(s) in the cost matrix by crossing out lines (rows/cols) with zeros in the cost matrix,
        then substracting/adding the smallest not crossed out value
    create_assignment(raw_assignment: Dict[int, int]) -> Assignment:
        creates an assignment instance based on the given dictionary assignment
    '''
    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)

    def solve(self) -> Assignment:
        costs = np.array(self.problem.costs)

        while True:
            self.extracts_mins(costs)
            max_assignment = self.find_max_assignment(costs)
            if len(max_assignment) == self.problem.size():
                return self.create_assignment(max_assignment)
            self.add_zero_by_crossing_out(costs, max_assignment)

    def extracts_mins(self, costs):
        #TODO: substract minimal values from each row and column
        for i in range(costs.shape[0]):
            min_value = np.min(costs[i, :])
            for j in range(costs.shape[1]):
                costs[i, j] = costs[i, j] - min_value

        for j in range(costs.shape[1]):
            min_value = np.min(costs[:, j])
            for i in range(costs.shape[0]):
                costs[i, j] = costs[i, j] - min_value

        return costs

    def add_zero_by_crossing_out(self, costs: np.array, partial_assignment: Dict[int,int]):
        #TODO:
        # 1) "mark" columns and rows according to the instructions given by teacher
        # 2) cross out marked columns and not marked rows
        # 3) find minimal uncrossed value and subtract it from the cost matrix
        # 4) add the same value to all crossed out columns and rows

        marked_rows = []
        marked_cols = []
        for i in range(costs.shape[0]):
            if not i in partial_assignment:
                marked_rows.append(i)

        change = True
        while change:
            change = False

            for row in marked_rows:
                for j in range(costs.shape[1]):
                    if costs[row, j] == 0:
                        if j not in marked_cols:
                            marked_cols.append(j)

            for col in marked_cols:
                for i in range(costs.shape[0]):
                    if i in partial_assignment:
                        if partial_assignment[i] == col:
                            if i not in marked_rows:
                                change = True
                                marked_rows.append(i)

        cros_row_without_mark = []
        cros_col_with_mark = marked_cols
        for i in range(costs.shape[0]):
            if i not in marked_rows:
                cros_row_without_mark.append(i)

        min_uc = np.max(costs)
        for i in range(costs.shape[0]):
            for j in range(costs.shape[1]):
                if (i not in cros_row_without_mark) and (j not in cros_col_with_mark):
                    if costs[i, j] < min_uc:
                        min_uc = costs[i, j]

        for i in range(costs.shape[0]):
            for j in range(costs.shape[1]):
                costs[i, j] = costs[i, j] - min_uc

        for row in cros_row_without_mark:
            for j in range(costs.shape[1]):
                costs[row, j] = costs[row, j] + min_uc

        for col in cros_col_with_mark:
            for i in range(costs.shape[0]):
                costs[i, col] = costs[i, col] + min_uc





    def find_max_assignment(self, costs) -> Dict[int,int]:
        #TODO: find the bigest assignment in the cost matrix
        # 1) always try the row with the least amount of 0s
        # 2) then column with least amount of 0s
        # TIP: remember, rows and cols can't repeat in the assignment
        rows_dict = {}
        cols_dict = {}
        result_dict = {}

        for i in range(costs.shape[0]):
            row = []
            for j in range(costs.shape[1]):
                if costs[i, j] == 0:
                    row.append(j)
            if len(row) > 0:
                rows_dict[i] = row
        for j in range(costs.shape[1]):
            col = []
            for i in range(costs.shape[0]):
                if costs[i, j] == 0:
                    col.append(i)
            if len(col) > 0:
                cols_dict[j] = col

        for iter in range(costs.shape[0]):
            min_row_index = -1
            for row_index, row in rows_dict.items():
                if min_row_index == -1:
                    min_row_index = row_index
                else:
                    if len(row) < len(rows_dict[min_row_index]):
                        min_row_index = row_index

            min_col_index = -1
            cols_in_min_row = rows_dict[min_row_index]

            for col_index, col in cols_dict.items():
                if col_index in cols_in_min_row:
                    if min_row_index in col:
                        if min_col_index == -1:
                            min_col_index = col_index
                        else:
                            if len(col) < len(cols_dict[min_col_index]):
                                min_col_index = col_index

            result_dict[min_row_index] = min_col_index

            for row_index, row in rows_dict.copy().items():
                if min_col_index in row:
                    row.remove(min_col_index)
                    if len(row) == 0:
                        rows_dict.pop(row_index)
            for col_index, col in cols_dict.copy().items():
                if min_row_index in col:
                    col.remove(min_row_index)
                    if len(col) == 0:
                        cols_dict.pop(col_index)
        return result_dict

    def create_assignment(self, raw_assignment: Dict[int,int]) -> Assignment:
        #TODO: create an assignment instance based on the dictionary
        # tips:
        # 1) use self.problem.original_problem.costs to calculate the cost
        # 2) in case the original cost matrix (self.problem.original_problem.costs wasn't square)
        #    and there is more workers than task, you should assign -1 to workers with no task

        org_n_workers = self.problem.original_problem.n_workers()
        org_n_tasks = self.problem.original_problem.n_tasks()
        n_workers, n_tasks = self.problem.costs.shape
        worker_tasks = [-1] * n_workers

        for worker, task in raw_assignment.items():
            if worker < org_n_workers and task < org_n_tasks:
                worker_tasks[worker] = task

        cost = 0
        for i in range(n_workers):
            if worker_tasks[i] >= 0:
                cost = cost + self.problem.original_problem.costs[i, worker_tasks[i]]

        return Assignment(worker_tasks, cost)

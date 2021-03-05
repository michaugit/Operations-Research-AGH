from copy import deepcopy
from . import model as m 
from .expressions import objective as o 
from .expressions import constraint as c
import numpy as np 

class Solution:
    """
        A class to represent a solution to linear programming problem.


        Attributes
        ----------
        model : Model
            model corresponding to the solution
        assignment : list[float]
            list with the values assigned to the variables
            order of values should correspond to the order of variables in model.variables list


        Methods
        -------
        __init__(model: Model, assignment: list[float]) -> Solution:
            constructs a new solution for the specified model and assignment
        value(var: Variable) -> float:
            returns a value assigned to the specified variable
        objective_value()
            returns value of the objective function
    """

    def __init__(self, model, assignment):
        "Assignment is just a list of values"
        self.assignment = assignment
        self.model = model

    def value(self, var):
        return self.assignment[var.index]

    def objective_value(self):
        return self.model.objective.evaluate(self.assignment)       

    def __str__(self):
        text = f'- objective value: {self.objective_value()}\n'
        text += '- assignment:'
        for (i,val) in enumerate(self.assignment):
            text += f'\n\t- {self.model.variables[i].name} = {val}'
        return text

class Tableaux:
    """
        A class to represent a solution to linear programming problem.


        Attributes
        ----------
        model : Model
            model corresponding to the tableaux
        table : numpy.Array
            2d-array with the tableaux

        Methods
        -------
        __init__(model: Model, solution: Solution) -> Tableaux:
            constructs a new tableaux for the specified model and solution
        cost_factors() -> numpy.Array:
            returns a vector containing factors in the cost row
        cost() -> float:
            returns the cost of solution represented in tableaux
        is_optimal() -> bool:
            checks whether the current solution is optimal
        choose_entering_variable() -> int:
            finds index of the variable, that should enter the basis next
        is_unbounded(col: int) -> bool:
            checks whether the problem is unbounded
        choose_leaving_variable(col: int) -> int:
            finds index of the variable, that should leave the basis next
        pivot(col: int, row: int):
            updates tableaux using pivot operation with given entering and leaving variables
        extract_solution() -> Solution:
            returns solution corresponding to the tableaux
        extract_basis() -> list[int]
            returns list of indexes corresponding to the variables belonging to the basis
    """

    def __init__(self, model):
        self.model = model
		# the "z column" is always constant so we don't include it in our table
        cost_row = np.array((-1 * model.objective.expression).factors(model) + [0.0])
        self.table = np.array([cost_row] + [c.expression.factors(model) + [c.bound] for c in model.constraints])
        #self._print(self.table)

    def _print(self, tableaux):
        print("tableaux:")
        for row in tableaux:
            print(''.join(str(x).ljust(7) for x in row))
        print("\n")

    def cost_factors(self):
        return self.table[0, :-1]

    def cost(self):
        return self.table[0, -1]

    def is_optimal(self):
        # TODO: 
        # if all factors in the cost row are >= 0
        for cell in self.cost_factors():
            if cell < 0:
                return False
        return True

    def choose_entering_variable(self):
        # TODO: 
        # return column index with the smallest factor in the cost row
        index = np.where(self.cost_factors() == np.amin(self.cost_factors()))[0][0]
        return index

    def is_unbounded(self, col):
        # TODO: 
        # if all factors in the specified column are <= 0
        for cell in self.table[:, col]:
            if cell > 0:
                return False
        return True


    def choose_leaving_variable(self, col):
        # TODO:
        # return row index associated with the leaving variable
        # to choose the row, divide beta column (last column) by the specified column
        # then choose a row index associated with the smallest positive value in the result
        # tip: take care to not divide by 0 :)
        last_column = self.table[+1:, -1:]
        column = self.table[+1:, col]
        result = []

        for i in range(len(last_column)):
            if column[i] != 0:
                x = last_column[i]/column[i]
                if x[0] > 0:
                    result.append([x[0], i])

        result = np.array(result)
        row_index = np.where(result[:, 0] == np.amin(result[:, 0]))[0][0]
        index = int(result[row_index, 1] + 1)

        return index

    def pivot(self, row, col):
        # TODO:
        # 1) the pivot row (row at index 'row') has to be devided by the old value of the table[row, col]
        # 2) the pivot column (column at index col) now belongs to basis and should contain only 0s 
        #    except the table[row,col] where it should equal 1 (already done in the first step)
        # 3) all other cells (neither in the pivot row nor column) are updated with the following rule:
        #    t'[r,c] = t[r,c] + (-t[r,col]) * t'[row, c]
        #    where:
        #       * t' = new tableaux
        #       * t = old tableaux
        #       * row, col = pivot row and columns accordingly
        #       * r, c = cell coordinates
        new_table = np.copy(self.table)
        old_table = self.table
        pivot = self.table[row, col]

        for index in range(len(new_table[row, :])):
            if pivot != 0:
                new_table[row, index] = new_table[row, index] / pivot

        for index in range(len(new_table[:, col])):
            if index != row:
                new_table[index, col] = 0

        for row_index in range(len(new_table)):
            for col_index in range(len(new_table[row_index])):
                if row_index != row and col_index != col:
                    new_table[row_index, col_index] = \
                        old_table[row_index, col_index] + ((- old_table[row_index, col]) * new_table[row, col_index])
        self.table = new_table


    def extract_solution(self):
        # TODO:
        # value of the variable in basis is the beta value (last column of the table)
        # belonging the row, where the variable has value 1.0
        # tip: extract_basis may be helpful
        last_column = (self.table[+1:, -1:])[:, 0]
        basis = self.extract_basis()
        assignment = [0] * (len(self.model.variables))

        for index in range(len(basis)):
            assignment[basis[index]] = last_column[index]

        return Solution(self.model, assignment)

    
    def extract_basis(self):
        rows_n, cols_n = self.table.shape
        basis = [-1 for _ in range(rows_n -1)]
        for c in range(cols_n - 1):
            column = self.table[:,c]
            belongs_to_basis = column.min() == 0.0 and column.max() == 1.0 and column.sum() == 1.0
            if belongs_to_basis:
                row = np.where(column == 1.0)[0][0]
                # [row-1] because we ignore the cost variable in the basis
                basis[row-1] = c
        return basis

    def __str__(self):
        def cell(x, w):
            return '{0: >{1}}'.format(x, w)

        cost_name = "z" if self.model.objective.factor > 0 else "-z"
        basis = self.extract_basis()
        header = ["basis", cost_name] + [var.name for var in self.model.variables] + ["b"]
        longest_col = max([len(h) for h in header])

        rows = [[cost_name]] + [[self.model.variables[i].name] for i in basis]

        for (i,r) in enumerate(rows):
            cost_factor = 0.0 if i > 0 else 1.0
            r += [str(v) for v in [cost_factor] + list(self.table[i])]
            longest_col = max(longest_col, max([len(v) for v in r]))

        header = [cell(h, longest_col) for h in header]
        rows = [[cell(v, longest_col) for v in row] for row in rows]

        cell_sep = " | "

        result = cell_sep.join(header) + "\n"
        for row in rows:
            result += cell_sep.join(row) + "\n"
        return result

class Solver:
    """
        A class to represent a simplex solver.

        Methods
        -------
        solve(model: Model) -> Solution:
            solves the given model and return the first solution
    """

    def solve(self, model):
        normal_model = self._normalize_model(deepcopy(model))
        tableaux = Tableaux(normal_model)

        while (not tableaux.is_optimal()):
            pivot_col = tableaux.choose_entering_variable()
            if tableaux.is_unbounded(pivot_col):
                raise Exception("Linear Programming model is unbounded")
            pivot_row = tableaux.choose_leaving_variable(pivot_col)

            tableaux.pivot(pivot_row, pivot_col)
        
        return tableaux.extract_solution()

    def _normalize_model(self, model):
        """
            _normalize_model(model: Model) -> Model:
                returns a normalized version of the given model 
        """
        if model.objective.type == o.ObjectiveType.MIN:
            model.objective.invert()
        
        self.slack_variables = dict()
        for (i,constraint) in enumerate(model.constraints):
            if constraint.type != c.ConstraintType.EQ:
                slack_var = model.create_variable(f"s{i}")
                self.slack_variables[slack_var.index] = i
                
                if constraint.bound < 0:
                    constraint.invert()
                
                constraint.expression = constraint.expression + slack_var * c.ConstraintType.LE.value * -1
                constraint.type = c.ConstraintType.EQ 
        return model


        
        
        
        
        
        


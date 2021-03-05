from copy import deepcopy

from saport.simplex.expressions.constraint import ConstraintType
from saport.simplex.expressions.objective import ObjectiveType
from saport.simplex.model import Model


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
        print(self.model)
        text = f'- objective value: {self.objective_value()}\n'
        text += '- assignment:\n'
        for (i,var) in enumerate(self.assignment):
            text += f'\t {self.model.variables[i].name} : {var}'
        return text

class Solver:
    """
        A class to represent a simplex solver.

        Methods
        -------
        solve(model: Model) -> Solution:
            solves the given model and return the first solution
    """

    def __init__(self):
        self.new_variables = 1

    def _print(self, tableaux):
        print("tableaux:")
        for row in tableaux:
            print(''.join(str(x).ljust(7) for x in row))
        print("\n")

    def solve(self, model):
        normal_model = self._normalize_model(deepcopy(model))
        solution = self._find_initial_solution(normal_model)
        tableaux = self._tableux(normal_model, solution)
        #TODO: 
        # - print normal model
        # - print initial solution
        # - print tableux

        self._print(tableaux)
        return solution

    def _normalize_model(self, model) -> Model:
        """
            _normalize_model(model: Model) -> Model:
                returns a normalized version of the given model 
        """
        #TODO: this method should create a new canonical model based on the current one
        # - canonical model has only the MAX objective
        # - canonical model has only EQ constraints (thanks to the additional slack / surplus variables)
        #   you should add extra (slack, surplus) variables and store them somewhere as the solver attribute
        normalized_model = model
        if normalized_model.objective.type == ObjectiveType.MIN:
            normalized_model.maximize(model.objective.expression)
            for i in range(0, len(normalized_model.objective.expression.atoms)):
                normalized_model.objective.expression.atoms[i].factor *= (-1)
        for x in normalized_model.constraints:

            v = normalized_model.create_variable(f's{self.new_variables}')
            if x.type == ConstraintType.LE:
                x.expression = x.expression + v
            else:
                x.expression = x.expression - v
            x.type = ConstraintType.EQ
            self.new_variables += 1

        return normalized_model

    def _find_initial_solution(self, model) -> Solution:
        """
        _find_initial_solution(model: Model) -> Solution
        returns an initial solution for the given model
        """
        #TODO: this method should find an initial feasible solution to the model
        # - should use the slack / surplus variables added during the normalization
        normalized_model = model
        assignment = [0] * (len(model.variables)-(self.new_variables-1))

        for x in normalized_model.constraints:
            assignment.append(x.bound)

        return Solution(model,assignment)

    def _tableux(self, model, solution):
        """
        _tableux(model: Model, solution: Solution) -> list[list[float]]
            returns a tableux for the given model and solution
        """
        #TODO: this method should create an array (list of lists is fine, but you can cahnge it) 
        # representing the tableux for the given model and solution

        normalized_model = model
        length_of_atoms = len(model.variables)
        length_of_constraints = len(normalized_model.constraints)
        s_index = len(model.variables) - (self.new_variables - 1)

        row_1_variables = [' ',' ']
        for i in range(0, length_of_atoms):
            row_1_variables.append(normalized_model.variables[i].name)
        row_1_variables.append(' ')

        row_2 = ["Cb","Z.baz"]
        for x in normalized_model.objective.expression.atoms:
            row_2.append(x.factor)
        for y in range(0, self.new_variables):
            row_2.append(0)

        divide_row = ['-------'] * (length_of_atoms+3)

        tableaux = [row_1_variables, row_2, divide_row]

        for i in range(0, length_of_constraints):
            _row = [0, normalized_model.variables[s_index + i].name]
            for j in range(0, s_index):
                _row.append(normalized_model.constraints[i].expression.atoms[j].factor)
            for s in range(0, (self.new_variables-1)):
                _row.append(0)
            _row.append(normalized_model.constraints[i].bound)
            _row[i+s_index+2] = normalized_model.constraints[i].expression.atoms[s_index].factor
            tableaux.append(_row)
        tableaux.append(divide_row)

        zj_table = [' ', 'Zj']
        for i in range(2, (len(tableaux[4]))):
            self.sum=0
            for j in range(0, length_of_constraints):
                self.sum += tableaux[j+3][0]*tableaux[j+3][i]
            zj_table.append(self.sum)
        tableaux.append(zj_table)

        cj_zj_table = [' ', 'Cj-Zj']
        for i in range(2, (len(tableaux[4]))):
            cj_zj_table.append(tableaux[1][i]-zj_table[i])
        tableaux.append(cj_zj_table)

        return tableaux
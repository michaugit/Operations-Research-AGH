from copy import deepcopy
from ..simplex import solver as lpsolver
from ..simplex import solution
import math
import time

from ..simplex.expressions.constraint import ConstraintType, Constraint
from ..simplex.expressions.expression import Expression
from ..simplex.solution import Solution


class Solver:
    """
        Naive branch and bound solver for integer programming problems


        Attributes
        ----------
        model : Model
            integer programming model to be solved
        timelimit: int
            what is the maximal solving time (in seconds)
        total_time: float
            how long it took to solve the problem
        start_time: float
            when the solving started
        interrupted: bool
            whether solving has been interrupted (by timeout)

        Methods
        -------
        start_timer():
            remember the starting time for the solver
        stop_timer():
            stores the total solving time
        wall_time() -> float:
            returns how long solver has been working
        timeout() -> bool:
            whether solver should stop working due to the timeout

        solve(model: Model, timelimit: int) -> Solution:
            solves the given model within a specified timelimit
        branch_and_bound(model: Model):
            processes given model in branch and bound fashion (recursively)
        find_float_assignment(solution: Solution):
            finds a variable with non-integer value in the current solution
            returns None if the solution is a correct integer solution
        model_with_new_constraint(self, model, constraint):
            creates a new model with an additional constraint
    """  

    def solve(self, model, timelimit):
        self.timelimit = timelimit
        self.total_time = None
        self.start_time = None
        self.interrupted = False

        self.model = model
        self.lower_bound = float('-inf')
        self.best_solution = None

        self.start_timer()
        self.branch_and_bound(model)
        self.stop_timer()

        return self.best_solution
           
    def branch_and_bound(self, model):
        #TODO: implement a branch and bound procedure
        # tip1: remember to check for the timeout and set te self.interrupted to True when it happens
        # tip2: remember to hande infeasible and unbounded models, check `simplex_examples` to know how to check for this condition
        if self.timeout():
            self.interrupted = True
            return

        simplex_solver = lpsolver.Solver()
        solution_of_visit = simplex_solver.solve(deepcopy(model))

        if not ((solution_of_visit.is_bounded is True) and (solution_of_visit.is_feasible is True)):
            return
        if self.lower_bound >= solution_of_visit.objective_value():
            return

        index = self.find_float_assignment(solution_of_visit)

        if index is None:
            self.lower_bound = solution_of_visit.objective_value()
            self.best_solution = solution_of_visit
            return
        else:
            value_of_variable = solution_of_visit.assignment[index]

            model_left = deepcopy(model)
            left_constraint_bound = math.ceil(value_of_variable)
            left_constraint_expression = Expression.from_vectors([model.variables[index]], [1])
            left_type_of_constraint = ConstraintType.GE
            model_left.add_constraint(Constraint(left_constraint_expression, left_constraint_bound, left_type_of_constraint))
            self.branch_and_bound(model_left)

            model_right = deepcopy(model)
            right_constraint_bound = math.floor(value_of_variable)
            right_constraint_expression = Expression.from_vectors([model.variables[index]], [1])
            right_type_of_constraint = ConstraintType.LE
            model_right.add_constraint(Constraint(right_constraint_expression, right_constraint_bound, right_type_of_constraint))
            self.branch_and_bound(model_right)

    def find_float_assignment(self, solution):
        #TODO: find an variable that has non-integer value in the solution
        # tip: due to numeric errors some variables can have "almost integer" value, like 0.9999999 or 1.0000001
        #      make sure they are still counted as integers
        for variable in self.model.variables:
            value = solution.assignment[variable.index]
            if not self.is_integer(value):
                return variable.index
        return None

    def is_integer(self, number, abs_tolerance=0.00000001):
        return (math.isclose(number, math.floor(number), abs_tol=abs_tolerance)) or (math.isclose(number, math.ceil(number), abs_tol=abs_tolerance))

    def model_with_new_constraint(self, model, constraint):
        new_model = deepcopy(model)
        new_model.add_constraint(constraint)
        return new_model

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        self.total_time = self.wall_time()

    def wall_time(self) -> float:
        return time.time() - self.start_time

    def timeout(self) -> bool:
        return self.wall_time() > self.timelimit

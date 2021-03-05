from ..abstractsolver import AbstractSolver
from ..model import Problem, Solution, Item
from typing import List 
from ...integer.model import Model
from ...simplex.expressions.constraint import ConstraintType, Constraint
from ...simplex.expressions.expression import Expression

class IntegerSolver(AbstractSolver):
    """
    An Integer Programming solver for the knapsack problems

    Methods:
    --------
    create_model() -> Models:
        creates and returns an integer programming model based on the self.problem
    """

    def create_model(self) -> Model:
        #TODO: create an integer programming model based on the problem

        model = Model("IntegerModel")

        for item in self.problem.items:
            model.create_variable("x" + item.index.__str__())

        constraint_factors = []
        objective_factors = []

        for item in self.problem.items:
            constraint_factors.append(item.weight)
            objective_factors.append(item.value)

        self.create_main_constraint(model, constraint_factors)
        self.create_objective_function(model, objective_factors)
        self.create_integer_constraint_for_each_variable(model)

        return model

    def create_main_constraint(self, model, constraint_factors):
        constraint_expression = Expression.from_vectors(model.variables, constraint_factors)
        bound = self.problem.capacity
        type_of_constraint = ConstraintType.LE
        model.add_constraint(Constraint(constraint_expression, bound, type_of_constraint))

    def create_objective_function(self, model, objective_factors):
        objective_expression = Expression.from_vectors(model.variables, objective_factors)
        model.maximize(objective_expression)

    def create_integer_constraint_for_each_variable(self, model):
        bound = 1
        factor = 1
        for var in model.variables:
            model.add_constraint(Constraint(Expression.from_vectors([var], [factor]), bound, ConstraintType.LE))

    def solve(self) -> Solution:
        m = self.create_model()
        integer_solution = m.solve(self.timelimit)
        items = [item for (i,item) in enumerate(self.problem.items) if integer_solution.value(m.variables[i]) > 0]
        solution = Solution.from_items(items, not m.solver.interrupted)
        self.total_time = m.solver.total_time
        return solution
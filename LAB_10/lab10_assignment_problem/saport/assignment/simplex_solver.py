import numpy as np
from .model import AssignmentProblem, Assignment, NormalizedAssignmentProblem
from ..simplex.expressions.constraint import Constraint, ConstraintType
from ..simplex.expressions.variable import Variable
from ..simplex.model import Model
from ..simplex.expressions.expression import Expression
from dataclasses import dataclass
from typing import List 



class Solver:
    '''
    A simplex solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    '''
    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)
        
    def solve(self) -> Assignment:
        model = Model("assignment")
        # TODO:
        # 1) creates variables, one for each cost in the cost matrix
        # 2) add constraint, that sum of every row has to be equal 1
        # 3) add constraint, that sum of every col has to be equal 1
        # 4) add constraint, that every variable has to be <= 1
        # 5) create an objective expression, involving all variables weighted by their cost
        # 6) add the objective to model (minimize it!)

        variables = np.zeros(self.problem.costs.shape, dtype=Variable)
        for i in range(self.problem.costs.shape[0]):
            for j in range(self.problem.costs.shape[1]):
                variables[i, j] = model.create_variable("X_"+str(i)+str(j))

        for i in range(self.problem.costs.shape[0]):
            c_vars = []
            c_factors = []

            for j in range(self.problem.costs.shape[1]):
                c_vars.append(variables[i, j])
                c_factors.append(1)

            bound = 1
            model.add_constraint(Constraint(Expression.from_vectors(c_vars, c_factors), bound, ConstraintType.EQ))

        for j in range(self.problem.costs.shape[1]):
            c_vars = []
            c_factors = []

            for i in range(self.problem.costs.shape[0]):
                c_vars.append(variables[i, j])
                c_factors.append(1)

            bound = 1
            model.add_constraint(Constraint(Expression.from_vectors(c_vars, c_factors), bound, ConstraintType.EQ))

        for i in range(self.problem.costs.shape[0]):
            for j in range(self.problem.costs.shape[1]):
                model.add_constraint(Constraint(Expression.from_vectors([variables[i, j]], [1]), 1, ConstraintType.LE))

        objective_vars = []
        objective_factors = []
        for i in range(self.problem.costs.shape[0]):
            for j in range(self.problem.costs.shape[1]):
                objective_vars.append(variables[i, j])
                objective_factors.append(self.problem.costs[i, j])

        model.minimize(Expression.from_vectors(objective_vars, objective_factors))

        solution = model.solve()

        # TODO:
        # 1) extract assignment for the original problem from the solution object
        # tips:
        # - remember that in the original problem n_workers() not alwyas equals n_tasks()
        org_n_workers = self.problem.original_problem.n_workers()
        org_n_tasks = self.problem.original_problem.n_tasks()
        n_workers, n_tasks = self.problem.costs.shape
        worker_tasks = [-1] * n_workers

        for i in range(len(solution.assignment)):
            index_of_worker = i // n_tasks
            index_of_task = i % n_workers
            if solution.assignment[i] == 1 and index_of_worker < org_n_workers and index_of_task < org_n_tasks:
                worker_tasks[index_of_worker] = index_of_task

        cost = 0
        for i in range(n_workers):
            if worker_tasks[i] >= 0:
                cost = cost + self.problem.original_problem.costs[i, worker_tasks[i]]

        return Assignment(worker_tasks, cost)




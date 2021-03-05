from dataclasses import dataclass
from .solver import AbstractSolver
from ..model import Game, Equilibrium, Strategy
from ...simplex import model as lpmodel
from ...simplex import solution as lpsolution
from ...simplex.expressions import expression as expr
import numpy as np
from typing import Tuple, List

from ...simplex.expressions.constraint import Constraint, ConstraintType
from ...simplex.expressions.expression import Expression


class MixedSolver(AbstractSolver):

    def solve(self) -> Equilibrium:
        shifted_game, shift = self.shift_game_rewards()

        # don't remove this print, it will be graded :)
        print(f"- shifted game: \n{shifted_game}")

        a_model = self.create_max_model(shifted_game)
        b_model = self.create_min_model(shifted_game)       
        a_solution = a_model.solve()
        b_solution = b_model.solve()

        a_probabilities = self.extract_probabilities(a_solution)
        b_probabilities = self.extract_probabilities(b_solution)

        # TODO: the correct Equilibirum instead of None
        return Equilibrium(a_solution.objective_value() - shift, Strategy(a_probabilities), Strategy(b_probabilities))

    def shift_game_rewards(self) -> Tuple[Game, float]:
        #TODO:
        # check if game value can be negative
        # if it's the case calculate the correct reward shift
        # to make it nonnegative

        matrix = self.game.reward_matrix
        min_from_matrix = np.amin(matrix)

        if min_from_matrix < 0:
            shift = abs(min_from_matrix)
        else:
            shift = 0

        return Game(self.game.reward_matrix + shift), shift

    def create_max_model(self, game: Game) -> lpmodel.Model:
        a_actions, b_actions = game.reward_matrix.shape

        a_model = lpmodel.Model("A")

        #TODO:
        # one variable for game value
        # + as many variables as there are actions available for player A
        # sum of those variables should be equal 1
        # for each column, value - column * actions <= 0
        # maximize value variable

        z = a_model.create_variable("z")
        a_model.maximize(z)



        for i in range(a_actions):
            a_model.create_variable("x" + i.__str__())

        probability_constraint_factors = [1] * a_actions
        probability_bound = 1
        probability_expression = Expression.from_vectors(a_model.variables[+1:], probability_constraint_factors)
        a_model.add_constraint(Constraint(probability_expression, probability_bound, ConstraintType.EQ))

        for i in range(b_actions):
            matrix_factors = game.reward_matrix[:, i]
            neg_constraint_factors = [-x for x in matrix_factors]
            constraint_factors = [1.0] + neg_constraint_factors

            expression = Expression.from_vectors(a_model.variables, constraint_factors)
            c_type = ConstraintType.LE
            bound = 0
            a_model.add_constraint(Constraint(expression, bound, c_type))

        return a_model

    def create_min_model(self, game: Game) -> lpmodel.Model:
        a_actions, b_actions = game.reward_matrix.shape

        b_model = lpmodel.Model("B")
        
        #TODO:
        # one variable for game value
        # + as many variables as there are actions available for playerBA
        # sum of those variables should be equal 1
        # for each row, value - row * actions >= 0
        # minimize value variable

        z = b_model.create_variable("z")
        b_model.minimize(z)

        for i in range(b_actions):
            b_model.create_variable("y" + i.__str__())

        probability_bound = 1
        probability_constraint_factors = [1] * b_actions
        probability_expression = Expression.from_vectors(b_model.variables[+1:], probability_constraint_factors)
        b_model.add_constraint(Constraint(probability_expression, probability_bound, ConstraintType.EQ))

        for i in range(a_actions):
            matrix_factors = game.reward_matrix[i, :]
            neg_constraint_factors = [-x for x in matrix_factors]
            constraint_factors = [1.0] + neg_constraint_factors

            expression = Expression.from_vectors(b_model.variables, constraint_factors)
            c_type = ConstraintType.GE
            bound = 0
            b_model.add_constraint(Constraint(expression, bound, c_type))

        return b_model

    def extract_probabilities(self, solution: lpsolution.Solution) -> List[float]:
        return [solution.value(x) for x in solution.model.variables if not solution.model.objective.depends_on_variable(solution.model, x)]


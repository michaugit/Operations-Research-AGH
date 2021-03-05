from dataclasses import dataclass
from .solver import AbstractSolver
from ..model import Game, Equilibrium, Strategy
from typing import List
import numpy as np

class PureSolver(AbstractSolver):

    def solve(self) -> List[Equilibrium]:
        # TODO: basic solver finding all pure equilibriums
        #      reminder:
        #      if max of the column is the same as min of the row
        #      it is an equilibrium
        #      in case there is no pure equilibrium - should return an empty list
        col_maxs = []
        row_mins = []
        matrix = self.game.reward_matrix

        for i in range(matrix.shape[0]):
            row_min_value = np.amin(matrix[i, :])
            for j_ in range(len(matrix[i, :])):
                if matrix[i, j_] == row_min_value:
                    row_mins.append(tuple([row_min_value, i, j_]))

        for j in range(matrix.shape[1]):
            col_max_value = np.amax(matrix[:, j])
            for i_ in range(len(matrix[:, j])):
                if matrix[i_, j] == col_max_value:
                    col_maxs.append(tuple([col_max_value, i_, j]))

        eq = list(set(col_maxs).intersection(set(row_mins)))
        equilibrium_list = []

        for element in eq:
            value, index_a, index_b = list(element)

            strategy_a = [0.0] * matrix.shape[0]
            strategy_b = [0.0] * matrix.shape[1]

            strategy_a[index_a] = 1.0
            strategy_b[index_b] = 1.0

            equilibrium_list.append(Equilibrium(value, Strategy(strategy_a), Strategy(strategy_b)))

        return equilibrium_list




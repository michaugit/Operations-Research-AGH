from numpy.core.arrayprint import format_float_positional
from ..abstractsolver import AbstractSolver
from ..model import Problem, Solution, Item
import time


class AbstractGreedySolver(AbstractSolver):
    """
    An abstract greedy solver for the knapsack problems.

    Methods:
    --------
    greedy_heuristic(item : Item) -> float:
        return a value representing how much the given items is valuable to the greedy algorithm
        bigger value > earlier to take in the backpack
    """

    def greedy_heuristic(self, item: Item) -> float:
        raise Exception("Greedy solver requires a heuristic!")

    def solve(self) -> Solution:
        #TODO: implement the greedy solving strategy
        #      1) sort items in the problem by the self.greedy_heuristic
        #      2) take as many as you can
        #      3) remember to replace the line below :)
        self.start_timer()
        sorted_items = sorted(self.problem.items, key=self.greedy_heuristic, reverse=True)

        now_value = 0
        now_weight = 0
        chosen_items = []

        for item in sorted_items:
            if now_weight + item.weight <= self.problem.capacity:
                chosen_items.append(item)
                now_value = now_value + item.value
                now_weight = now_weight + item.weight

        self.stop_timer()
        return Solution(items=chosen_items, value=now_value, weight=now_weight, optimal=False)
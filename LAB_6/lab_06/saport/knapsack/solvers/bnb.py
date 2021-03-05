from ..abstractsolver import AbstractSolver
from ..model import Problem, Solution, Item
from typing import List 
class AbstractBnbSolver(AbstractSolver):
    """
    An abstract branch-and-bound solver for the knapsack problems.

    Methods:
    --------
    upper_bound(left : List[Item], solution: Solution) -> float:
        given the list of still available items and the current solution,
        calculates the linear relaxation of the problem
    """
    
    def upper_bound(self, left : List[Item], solution: Solution) -> float:
        #TODO: implement the linear relaxation, i.e. assume you can take   
        #      fraction of the items in the backpack
        #      return the value of such a solution
        #      tip1: solution is your starting point
        #      tip2: left is the list of items you can still take

        sorted_items = sorted(left, key=lambda it: it.value/it.weight, reverse=True)
        value = solution.value
        weight = solution.weight
        for item in sorted_items:
            if weight + item.weight <= self.problem.capacity:
                weight = weight + item.weight
                value = value + item.value
            else:
                diff = self.problem.capacity - weight
                how_much = diff / item.weight
                value = value + (item.value * how_much)
                break

        return value

        
    def solve(self) -> Solution:
        raise Exception("this is an abstract solver, don't try to run it!")
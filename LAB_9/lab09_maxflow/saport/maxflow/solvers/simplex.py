from .solver import AbstractSolver
from ...simplex.expressions.constraint import ConstraintType, Constraint
from ...simplex.model import Model as LinearModel
from ...simplex.expressions.expression import Expression as LinearExpression, Expression
from ..model import Network 

class SimplexSolver(AbstractSolver):

    def solve(self) -> int:
        m = LinearModel(self.network.name)

        #TODO:
        # 1) add one var per edge
        # 2) each var has to <= than the capacity of the corresponding edge
        # 3) the sum of flows going into a common node (not sink/not source) must be equal 0
        # tip: you also should ignore edges ending at source node / starting sink node
        # 4) you have to maximize sum of flows going from the source node

        digraph = self.network.digraph
        vars_start_end = {}
        start_end_vars = {}

        for edge in digraph.edges:
            variable = m.create_variable("e" + str(edge))
            vars_start_end[variable.name] = list(edge)
            start_end_vars[str(list(edge))] = variable

        for var in m.variables:
            start = vars_start_end[var.name][0]
            end = vars_start_end[var.name][1]

            bound = self.network.capacity(digraph, start, end)
            factor = 1
            m.add_constraint(Constraint(Expression.from_vectors([var], [factor]), bound, ConstraintType.LE))

        for node in digraph.nodes:
            if node != self.network.source_node and node != self.network.sink_node:
                in_edges = digraph.in_edges(node)
                out_edges = digraph.out_edges(node)

                variables = []
                factors = []
                bound = 0

                for edge in in_edges:
                    variables.append(start_end_vars[str(list(edge))])
                    factors.append(1)

                for edge in out_edges:
                    variables.append(start_end_vars[str(list(edge))])
                    factors.append(-1)

                m.add_constraint(Constraint(Expression.from_vectors(variables, factors), bound, ConstraintType.EQ))

        source_edges_out = digraph.out_edges(self.network.source_node)
        o_vars = []
        o_factors = []
        for edge in source_edges_out:
            o_vars.append(start_end_vars[str(list(edge))])
            o_factors.append(1)

        source_edges_in = digraph.in_edges(self.network.source_node)
        for edge in source_edges_in:
            o_vars.append(start_end_vars[str(list(edge))])
            o_factors.append(-1)

        objective_expr = Expression.from_vectors(o_vars, o_factors)
        m.maximize(objective_expr)

        solution = m.solve()
        return int(solution.objective_value())






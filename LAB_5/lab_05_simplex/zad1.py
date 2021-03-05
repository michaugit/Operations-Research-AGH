import logging
import math

from saport.simplex import solution
from saport.simplex.analyser import Analyser
from saport.simplex.analysis_tools.objective_sensitivity import ObjectiveSensitivityAnalyser
from saport.simplex.model import Model


def run():
    primal = Model("Zad1")

    # x1 -> SS - super
    # x2 -> S - standardowy
    # x3 -> O - oszczędny


    x1 = primal.create_variable("x1")
    x2 = primal.create_variable("x2")
    x3 = primal.create_variable("x3")

    primal.add_constraint(2*x1 + 2*x2 + 5*x3 <= 40)
    primal.add_constraint(x1 + 3*x2 + 2*x3 <= 30)
    primal.add_constraint(3*x1 + x2 + 3*x3 <= 30)

    primal.maximize(32*x1 + 24*x2 + 48*x3)

    expected_dual = Model("Zad1")

    y1 = expected_dual.create_variable("y1")
    y2 = expected_dual.create_variable("y2")
    y3 = expected_dual.create_variable("y3")

    expected_dual.add_constraint(2*y1 + y2 + 3*y3 >= 32)
    expected_dual.add_constraint(2*y1 + 3*y2 + y3 >= 24)
    expected_dual.add_constraint(5*y1 + 2*y2 + 3*y3 >= 48)

    expected_dual.minimize(40*y1 + 30*y2 + 30*y3)

    expected_bounds = [(19.6363636363, 44.57142857), (17.77777777, 53.333333333), (37.0, 61.99999999999)]









    dual = primal.dual()
    assert dual.is_equivalent(expected_dual), "dual wasn't calculated as expected"
    assert primal.is_equivalent(dual.dual()), "double dual should equal the initial model"

    primal_solution = primal.solve()
    dual_solution = dual.solve()
    assert math.isclose(primal_solution.objective_value(), dual_solution.objective_value(), abs_tol=0.000001), "dual and primal should have the same value at optimum"

    logging.info("Congratulations! The dual creation seems to be implemented correctly :)\n")

    analyser = Analyser()
    analysis_results = analyser.analyse(primal_solution)
    analyser.interpret_results(primal_solution, analysis_results, logging.info)

    objective_analysis_results = analysis_results[ObjectiveSensitivityAnalyser.name()]
    tolerance = 0.001

    for (i, bounds_pair) in enumerate(objective_analysis_results):
        assert math.isclose(bounds_pair[0], expected_bounds[i][0],
                            abs_tol=tolerance), f"left bound of the coefficient range seems to be incorrect, expected {expected_bounds[i][0]}, got {bounds_pair[0]}"
        assert math.isclose(bounds_pair[1], expected_bounds[i][1],
                            abs_tol=tolerance), f"right bound of the coefficient range seems to be incorrect, expected {expected_bounds[i][1]}, got {bounds_pair[1]}"

    logging.info("Congratulations! This cost coefficients analysis look alright :)")


    print(dual)
    print(analyser.interpret_results(primal_solution, analysis_results))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()

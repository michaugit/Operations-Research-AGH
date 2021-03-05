import logging
import math

from saport.simplex import solution
from saport.simplex.analyser import Analyser
from saport.simplex.analysis_tools.objective_sensitivity import ObjectiveSensitivityAnalyser
from saport.simplex.model import Model


def run():
    primal = Model("Zad2")

    # x1 -> ławki
    # x2 -> stoły
    # x3 -> krzesła

    x1 = primal.create_variable("x1")
    x2 = primal.create_variable("x2")
    x3 = primal.create_variable("x3")

    primal.add_constraint(8*x1 + 6*x2 + x3 <= 960)
    primal.add_constraint(8*x1 + 4*x2 + 3*x3 <= 800)
    primal.add_constraint(4*x1 + 3*x2 + x3 <= 320)

    primal.maximize(60*x1+30*x2+20*x3)

    expected_dual = Model("Zad2")

    y1 = expected_dual.create_variable("y1")
    y2 = expected_dual.create_variable("y2")
    y3 = expected_dual.create_variable("y3")

    expected_dual.add_constraint(8*y1 + 8*y2 + 4*y3 >= 60)
    expected_dual.add_constraint(6*y1 + 4*y2 + 3*y3 >= 30)
    expected_dual.add_constraint(y1 + 3*y2 + y3 >= 20)

    expected_dual.minimize(960*y1 + 800*y2 + 320*y3)

    expected_bounds = [(56.0, 80.0), (float("-inf"), 35.0), (15.0, 22.5)]









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

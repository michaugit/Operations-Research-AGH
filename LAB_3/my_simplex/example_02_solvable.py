import logging
from saport.simplex.model import Model 

def run():
    #TODO:
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * minimize the objective (so the solver would have to normalize it)
    # * make some "=>" constraints
    # * the model still has to be solvable by the basix simplex withour artificial variables
    # 
    # TIP: you may use other solvers (e.g. https://online-optimizer.appspot.com)
    #      to find the correct solution

    model = Model("example_02_solvable")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")
    x4 = model.create_variable("x4")

    model.add_constraint(-2*x1 - 4*x2 - 3*x3 - 7*x4 >= -800)
    model.add_constraint(-4*x1 - 5*x2 - 3*x3 - 2*x4 >= -640)
    model.add_constraint(-4*x1 - 1*x2 - 4*x3 - 1*x4 >= -600)

    model.minimize(-80*x1 - 60*x2 - 30*x3 - 50*x4)

    try:
        solution = model.solve()
    except:
        raise AssertionError("This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)

    assert (solution.assignment == [120.0, 0, 0, 80.0, 0.0, 0.0, 40]), "Your algorithm found an incorrect solution!"

    logging.info("Congratulations! This solution seems to be alright :)")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()

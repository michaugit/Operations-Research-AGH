import logging

from saport.simplex.model import Model


def run():
    #TODO:
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * make the model unbounded!
    # 
    # TIP: you may use other solvers (e.g. https://online-optimizer.appspot.com)
    #      to check if the problem is unbounded

    # logging.info("This test is empty but it shouldn't be, fix it!")
    # raise AssertionError("Test is empty")

    model = Model("example_03_unbounded")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")

    model.add_constraint(x1 - x2 + x3 <= 5)
    model.add_constraint(-2*x1 + x2 <= 3)
    model.add_constraint(x2 - 2*x3 <= 5)

    model.maximize(3*x2 + x3)

    try:
        solution = model.solve()
    except Exception as e:
        logging.info("Solver throw an Exception: " + e.__str__())
        # raise AssertionError(e.__str__())
        assert (e.__eq__("Linear Programming model is unbounded")), "Your algorithm throw an Exception -> \"Linear Programming model is unbounded\""

    logging.info("Congratulations! This Exception seems to be alright :)")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()

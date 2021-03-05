# TODO: model and solve assignment 3 from the PDF

# How to use SAPORT?

from saport.simplex.solver import Solver
from saport.simplex.model import Model

model = Model("Zadanie 3")

x1 = model.create_variable("steki")
x2 = model.create_variable("ziemniaki")

expr1 = 5 * x1 + 15 * x2
expr2 = 20 * x1 + 5 * x2
expr3 = 15 * x1 + 2 * x2

model.add_constraint(expr1 >= 50)
model.add_constraint(expr2 >= 40)
model.add_constraint(expr3 <= 60)

model.minimize(8 * x1 + 4 * x2)

print("Before solving:")
print(model)

solution = model.solve()

print("Solution: ")
print(solution)

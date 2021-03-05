# TODO: model and solve assignment 2 from the PDF

from saport.simplex.solver import Solver
from saport.simplex.model import Model


model = Model("Zadanie 2")

x1 = model.create_variable("p1")
x2 = model.create_variable("p2")
x3 = model.create_variable("p3")
x4 = model.create_variable("p4")

expr1 = 0.8 * x1 + 2.4 * x2 + 0.9 * x3 + 0.4 * x4
expr2 = 0.6 * x1 + 0.6 * x2 + 0.3 * x3 + 0.3 * x4

model.add_constraint(expr1 >= 1200)
model.add_constraint(expr2 >= 600)

model.minimize(9.6 * x1 + 14.4 * x2 + 10.8 * x3 + 7.2 * x4)

print("Before solving:")
print(model)

solution = model.solve()

print("Solution: ")
print(solution)

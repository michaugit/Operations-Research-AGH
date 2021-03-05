# TODO: model and solve assignment 1 from the PDF
# How to use SAPORT?

# 1. Import the library
from saport.simplex.solver import Solver
from saport.simplex.model import Model

model = Model("Zadanie 1")

x1 = model.create_variable("x1")
x2 = model.create_variable("x2")
x3 = model.create_variable("x3")

expr1 = x1 + x2 + x3
expr2 = x1 + 2*x2 + x3
expr3 = 2*x2 + x3

model.add_constraint(expr1 <= 30)
model.add_constraint(expr2 >= 10)
model.add_constraint(expr3 <= 20)

model.maximize(2* x1 + x2 + 3* x3)

print("Before solving:")
print(model)

solution = model.solve()

print("Solution: ")
print(solution)

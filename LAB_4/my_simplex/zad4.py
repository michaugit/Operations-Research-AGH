# TODO: model and solve assignment 4 from the PDF
# How to use SAPORT?

from saport.simplex.solver import Solver
from saport.simplex.model import Model

model = Model("Zadanie 4")

# LICZBA SPOSOBÓW OGRANICZONA DO 5 PONIEWAŻ INNE NIE MAJĄ SENSU I MOŻNA JE ODRZUCIC
x1 = model.create_variable("sps_1") #1x 105cm + 1x 75cm + 0x35cm => odpad: 20
x2 = model.create_variable("sps_2") #1x 105cm + 0x 75cm + 2x35cm => odpad: 25
x3 = model.create_variable("sps_3") #0x 105cm + 2x 75cm + 1x35cm => odpad: 15
x4 = model.create_variable("sps_4") #0x 105cm + 1x 75cm + 3x35cm => odpad: 20
x5 = model.create_variable("sps_5") #0x 105cm + 0x 75cm + 5x35cm => odpad: 25

expr1 = x1 + x2
expr2 = x1 + 2*x3 + x4
expr3 = 2*x2 + x3 + 3*x4 + 5*x5

model.add_constraint(expr1 == 150)
model.add_constraint(expr2 == 200)
model.add_constraint(expr3 == 150)

model.minimize(20*x1+25*x2+15*x3+20*x4+25*x5)

print("Before solving:")
print(model)

solution = model.solve()

print("Solution: ")
print(solution)


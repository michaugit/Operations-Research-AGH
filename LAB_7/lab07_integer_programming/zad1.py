from saport.integer.model import Model 

m = Model("Sense of Life")

# TODO: create variables, add constraints, set objective, etc.
x1 = m.create_variable("x1")
x2 = m.create_variable("x2")
x3 = m.create_variable("x3")
x4 = m.create_variable("x4")
x5 = m.create_variable("x5")
x6 = m.create_variable("x6")

m.add_constraint(2.15*x1 + 2.75*x2 + 3.35*x3 + 3.55*x4 + 4.20*x5 + 5.80*x6 <= 50)
m.add_constraint(x1 <= 5)
m.add_constraint(x2 <= 6)
m.add_constraint(x3 <= 7)
m.add_constraint(x4 <= 5)
m.add_constraint(x5 <= 1)
m.add_constraint(x6 <= 1)

m.maximize(3*x1 + 4*x2 + 4.5*x3 + 4.65*x4 + 8*x5 + 9*x6)

solution = m.solve()

print(m)
print(solution)
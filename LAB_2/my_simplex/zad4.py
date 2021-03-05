# How to use SAPORT?

# 1. Import the library
from saport.simplex.solver import Solver
from saport.simplex.model import Model

# 2. Create a model
model = Model("Zadanie 4")

# 3. Add variables
x1 = model.create_variable("sps_1")
x2 = model.create_variable("sps_2")
x3 = model.create_variable("sps_3")
x4 = model.create_variable("sps_4")
x5 = model.create_variable("sps_5")


# 4. FYI: You can create expression and evaluate them
expr1 = x1   + x2   +0*x3 + 0*x4 + 0*x5
expr2 = x1   + 0*x2 +2*x3 + x4   + 0*x5
expr3 = 0*x1 + 2*x2 +x3   + 3*x4 + 5*x5
#print(f"Value of the expression for the specified assignment is  {expr1.evaluate([1, 2,3,4,5,6,7,8,9,10,11,12,13,14,15])}\n")

# 5. Then add constraints to the model
model.add_constraint(expr1 >= 150)
model.add_constraint(expr2 >= 200)
model.add_constraint(expr3 >= 150)


# 6. Set the objective!
model.minimize(20*x1+25*x2+15*x3+20*x4+25*x5)


# 7. You can print the model
print("Before solving:")
print(model)

# 8. And finally solve it!
solution = model.solve()

# 9. Model is being simplified before being solver
# print("After solving:")
# print(model)

# 10. Print solution (uncomment after finishing assignment)
print("Solution: ")
print(solution)



# Placeholder for the assignment, refer to the example.py for tips # Placeholder for the assignment, refer to the example.py for tips 
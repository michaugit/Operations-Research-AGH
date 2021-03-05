# How to use SAPORT?

# 1. Import the library
from saport.simplex.solver import Solver
from saport.simplex.model import Model

# 2. Create a model
model = Model("Zadanie 3")

# 3. Add variables
x1 = model.create_variable("steki")
x2 = model.create_variable("ziemniaki")


# 4. FYI: You can create expression and evaluate them
expr1 = 5*x1 + 15*x2
expr2 = 20*x1 + 5*x2
expr3 = 15*x1 + 2*x2
 
print(f"Value of the expression for the specified assignment is  {expr1.evaluate([1, 1, 2])}\n")

# 5. Then add constraints to the model
model.add_constraint(expr1 >= 50)
model.add_constraint(expr2 >= 40)
model.add_constraint(expr3 <= 60)


# 6. Set the objective!
model.minimize(8*x1 + 4*x2)


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


# Placeholder for the assignment, refer to the example.py for tips 
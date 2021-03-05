# How to use SAPORT?

# 1. Import the library
from saport.simplex.solver import Solver
from saport.simplex.model import Model

# 2. Create a model
model = Model("Zadanie 2")

# 3. Add variables
x1 = model.create_variable("p1")
x2 = model.create_variable("p2")
x3 = model.create_variable("p3")
x4 = model.create_variable("p4")

# 4. FYI: You can create expression and evaluate them
expr1 = 0.8*x1 + 2.4*x2 + 0.9*x3 + 0.4*x4
expr2 = 0.6*x1 + 0.6*x2 + 0.3*x3 + 0.3*x4
 
#print(f"Value of the expression for the specified assignment is  {expr1.evaluate([1, 1, 2])}\n")

# 5. Then add constraints to the model
model.add_constraint(expr1 >= 1200)
model.add_constraint(expr2 >= 600)



# 6. Set the objective!
model.minimize(9.6*x1 + 14.4*x2 + 10.8*x3 + 7.2*x4)


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
from pulp import LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable

# Create the LP problem instance
problem = LpProblem("Linear_Programming_Problem", LpMinimize)  # or LpMaximize for maximization

# Define the decision variables
x = LpVariable("x", lowBound=0)  # Example variable
y = LpVariable("y", lowBound=0)  # Example variable

# Define the objective function
# Example: Minimize 2x + 3y
objective_function = 2 * x + 3 * y
problem += objective_function

# Add constraints
# Example: 3x + 4y >= 10
constraint1 = 3 * x + 4 * y >= 10
problem += constraint1

# Example: x + y <= 6
constraint2 = x + y <= 6
problem += constraint2

# Solve the LP problem
status = problem.solve()

# Print the status of the solution
print("Status:", LpStatus[status])

# Print the optimal solution
for variable in problem.variables():
    print(f"{variable.name} = {variable.varValue}")

# Print the optimal objective value
print("Optimal Objective Value:", problem.objective.value())

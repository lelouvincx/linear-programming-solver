from scipy.optimize import linprog

# Define the coefficients of the objective function
c = [-10, -20, -15]  # Coefficients to minimize

# Define the inequality constraints
A = [[1, 1, 1],  # Coefficients of x1, x2, x3 in the first constraint
     [-1, 0, 0],  # Coefficients of x1, x2, x3 in the second constraint
     [0, -1, 0],  # Coefficients of x1, x2, x3 in the third constraint
     [0, 0, -1]]  # Coefficients of x1, x2, x3 in the fourth constraint
b = [100, -50, -60, -40]  # Right-hand side values of the constraints

# Define the bounds for the variables
x_bounds = [(0, None), (0, None), (0, None)]  # Non-negative constraints for x1, x2, x3

# Solve the linear programming problem
result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds)

# Print the solution status
print("Status:", result.message)

# Print the optimal solution
print("Optimal Solution:")
for i, var in enumerate(result.x):
    print(f"x{i+1} =", var)

# Print the optimal objective value
print("Total Cost =", -result.fun)  # Multiply the objective value by -1 to get the minimized cost

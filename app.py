import streamlit as st
from pulp import LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable

st.set_page_config(
    page_title="Linear Programming Solver",
    page_icon="📔",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title("The Ultimate Linear Programming Problem Solver")

# Settings
st.title("Settings")

# Problem Type
st.markdown("### Choose the type of problem you want to solve:")
problem_type = st.radio("Problem Type", ("Maximization", "Minimization"), index=0)
# Create problem instance
problem = None
if problem_type == "Maximization":
    problem = LpProblem("Linear_Programming_Problem", LpMaximize)
else:
    problem = LpProblem("Linear_Programming_Problem", LpMinimize)

# Number of Decision Variables
st.markdown("### Choose the number of decision variables:")
num_vars = st.slider("Number of Decision Variables", 1, 10, 2, 1)
# Create list var with num_vars elements
var = [None] * num_vars
# Create num_vars variables
for i in range(num_vars):
    st.markdown(f"### Input constraints for variable x{i+1}:")
    var_name = f"x{i+1}"

    var_lower_bound = None
    # Create a selectbox for lower bound
    option_lower_bound = st.selectbox(
        f"Lower Bound of Decision Variable x{i+1}:",
        ("Negative Infinity", "Number")
    )
    if option_lower_bound == "Number":
        var_lower_bound = st.number_input(
            f"Lower Bound of Decision Variable x{i+1}:", value=0
        )
    else:
        var_lower_bound = None

    var_upper_bound = None
    # Create a selectbox for upper bound
    option_upper_bound = st.selectbox(
        f"Upper Bound of Decision Variable x{i+1}:",
        ("Positive Infinity", "Number")
    )
    if option_upper_bound == "Number":
        var_upper_bound = st.number_input(
            f"Upper Bound of Decision Variable x{i+1}:", value=10
        )
    else:
        var_upper_bound = None

    # Write a latex equation lower bound <= variable <= upper bound
    if var_lower_bound is not None and var_upper_bound is not None:
        st.latex(f"{var_lower_bound} \\leq {var_name} \\leq {var_upper_bound}")
    elif var_lower_bound is not None:
        st.latex(f"{var_lower_bound} \\leq {var_name} \\leq \\infty")
    elif var_upper_bound is not None:
        st.latex(f"-\\infty \\leq {var_name} \\leq {var_upper_bound}")
    else:
        st.latex(f"-\\infty \\leq {var_name} \\leq \\infty")

    var[i] = LpVariable(var_name, lowBound=var_lower_bound, upBound=var_upper_bound)

# Objective Function
st.markdown("Input the objective function:")
objective_function = ""
# Create objective function input
objective_function = st.text_input(
    "Objective Function (e.g. 2*x1 + 3*x2):", value="2*x1 + 3*x2"
)
# Replace x1, x2, ... with the variables
for i in range(num_vars):
    objective_function = objective_function.replace(f"x{i+1}", f"var[{i}]")
st.write(objective_function)
# Add objective function to problem
problem += eval(objective_function)

# Add constraints
constraints = []
st.markdown("Choose the number of constraints:")
num_constraints = st.slider("Number of Constraints", 1, 10, 2, 1)
# Create num_constraints input
for i in range(num_constraints):
    constraints.append(
        st.text_input(
            f"Constraint {i+1} (e.g. 3*x1 + 4*x2 >= 10):", value="3*x1 + 4*x2 >= 10"
        )
    )
# Replace x1, x2, ... with the variables
for i in range(num_vars):
    for j in range(num_constraints):
        constraints[j] = constraints[j].replace(f"x{i+1}", f"var[{i}]")
st.write(constraints)
# Add constraints to problem
for constraint in constraints:
    problem += eval(constraint)

# Write the problem
st.markdown("## Problem")
st.code(str(problem))


# Solve the LP problem
status = problem.solve()

st.markdown("## Solution")
st.write(f"Status: {LpStatus[status]}")
for i in range(num_vars):
    st.write(f"x{i+1}: {var[i].value()}")
st.write(f"Optimal Objective Value: {problem.objective.value()}")

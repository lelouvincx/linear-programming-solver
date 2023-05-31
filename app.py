"""
This is main file for processing.
And is called from streamlit to show on the web UI.
"""


import streamlit as st
# from utils import LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable
from pulp import LpProblem, LpVariable
from utils import LpMaximize, LpMinimize, LpStatus, LpSolution


st.set_page_config(
    page_title="Giải quy hoạch tuyến tính online",
    page_icon="📔",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.title("Giải quy hoạch tuyến tính online")

# Settings
st.markdown("## I. Hướng dẫn")
st.sidebar.title("⚙ Cài đặt")
st.sidebar.subheader("Thành viên")
st.sidebar.markdown("""
    | Name | Student ID | Leader | Note |
    |---|---|---|---|
    | Dinh Minh Chinh | 21280007 | x | |
    | Nguyen Trong Nhan | 21280038 | | |
""")


# Problem Type use 2 columns
st.markdown("### 1. Chọn loại bài toán")
col1, col2 = st.columns(2)
with col1:
    st.markdown("Có 2 loại bài toán:")
    st.markdown("- **Tối thiểu hóa**: Tìm giá trị nhỏ nhất của hàm mục tiêu - Minimization")
    st.markdown("- **Tối ưu hóa**: Tìm giá trị lớn nhất của hàm mục tiêu - Maximization")
    st.markdown("Hãy chọn loại bài toán bằng cách chọn một trong 2 nút bên cạnh.")

# st.sidebar.markdown("### Chọn hàm mục tiêu")
with col2:
    problem_type = st.radio("Loại bài toán:", ("Minimization", "Maximization"), index=0)

# Create problem instance
problem = None
if problem_type == "Maximization":
    problem = LpProblem("Linear_Programming_Problem", LpMaximize)
else:
    problem = LpProblem("Linear_Programming_Problem", LpMinimize)


# Number of Decision Variables
st.markdown("### 2. Chọn số lượng biến")
st.markdown("Hãy kéo thả thanh dưới đây đến số lượng biến cần tạo. Sau đó điền ràng buộc cho từng biến")

# st.sidebar.markdown("### Choose the number of decision variables:")
num_vars = st.slider("Số lượng biến", 1, 10, 2, 1)
cols = st.columns(num_vars)

# Create list var with num_vars elements
var = [None] * num_vars

# Create num_vars variables
for i in range(num_vars):
    with cols[i]:
        var_name = f"x{i+1}"

        var_lower_bound = None
        # Create a selectbox for lower bound
        option_lower_bound = st.selectbox(
            f"Cận dưới của biến x{i+1}:",
            ("Âm vô cùng", "Khác"),
            index=1
        )
        if option_lower_bound == "Khác":
            var_lower_bound = st.number_input(
                f"Cận dưới của biến x{i+1}:", value=0
            )
        else:
            var_lower_bound = None

        var_upper_bound = None
        # Create a selectbox for upper bound
        option_upper_bound = st.selectbox(
            f"Cận trên của biến x{i+1}:",
            ("Dương vô cùng", "Khác")
        )
        if option_upper_bound == "Khác":
            var_upper_bound = st.number_input(
                f"Cận trên của biến x{i+1}:", value=10
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
st.markdown("### 3. Hàm mục tiêu")
col1, col2 = st.columns(2)

with col2:
    st.markdown("Điền hàm mục tiêu vào ô bên dưới. Hãy sử dụng các biến đã tạo ở bước trước.")
    st.markdown("Ví dụ muốn nhập hàm mục tiêu: -x1 - 3*x2")
    st.markdown("- Các dấu nhân (*) không được bỏ qua")
    st.markdown("- Các cấu giữa 2 biến phải cách nhau bởi dấu cách")
    st.markdown("- Dấu '-' ở trước biến đầu tiên không cần dấu cách")

with col1:
    objective_function = ""
    # Create objective function input
    objective_function = st.text_input(
        "Hàm mục tiêu (e.g. -x1 - 3*x2):", placeholder="-x1 - 3*x2"
    )

# Replace x1, x2, ... with the variables
for i in range(num_vars):
    objective_function = objective_function.replace(f"x{i+1}", f"var[{i}]")
# Add objective function to problem
if objective_function != "":
    problem += eval(objective_function)

# Add constraints
st.markdown("### 4. Ràng buộc")
constraints = []
st.markdown("Hãy kéo thả thanh dưới đây đến số lượng ràng buộc cần tạo.")
num_constraints = st.slider("Số ràng buộc", 1, 10, 2, 1)
# Create num_constraints input
for i in range(num_constraints):
    constraints.append(
        st.text_input(
            f"Ràng buộc {i+1} (e.g. 3*x1 + 4*x2 >= 10):", placeholder="3*x1 + 4*x2 >= 10"
        )
    )
# Replace x1, x2, ... with the variables
for i in range(num_vars):
    for j in range(num_constraints):
        constraints[j] = constraints[j].replace(f"x{i+1}", f"var[{i}]")
# Add constraints to problem
for constraint in constraints:
    if constraint is not None and constraint != "":
        problem += eval(constraint)


# Write the problem
st.markdown("## Bài toán")
st.code(str(problem))


# Solve the LP problem
status = problem.solve()

# Result
st.markdown("## Bài giải")
st.info(f"Giải được: {LpSolution[status]}")
if st.button("Click để giải bài toán"):
    st.balloons()
    st.info(f"Trạng thái: {LpStatus[status]}")
    if status == 1: # Optimal
        st.markdown("#### Thông tin nghiệm:")
        for i in range(num_vars):
            st.markdown(f"- x{i+1} = {var[i].value()}")
        try:
            st.info(f"Nghiệm tối ưu: {problem.objective.value()}")
        except Exception as e:
            st.exception(e)
        else:
            st.success("Giải thành công!")
    elif status == -2: # Unbounded
        if problem_type == "Maximization":
            st.info(f"Giá trị tối ưu: $\\infty$")
        else:
            st.info(f"Giá trị tối ưu: $-\\infty$")

    if st.button("Giải tiếp"):
        st.experimental_rerun()

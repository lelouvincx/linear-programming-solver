"""
This is a file for utility functions. Used in app.py
The target is to provide functions to solve a linear programming problem.

Exported classes:
LpStatus
"""


from collections import Counter
import sys, warnings
from time import time

# variable categories
LpContinuous = "Continuous"
LpInteger = "Integer"
LpBinary = "Binary"
LpCategories = {LpContinuous: "Continuous", LpInteger: "Integer", LpBinary: "Binary"}

# objective sense
LpMinimize = 1
LpMaximize = -1
LpSenses = {LpMaximize: "Maximize", LpMinimize: "Minimize"}
LpSensesMPS = {LpMaximize: "MAX", LpMinimize: "MIN"}

# problem status
LpStatusNotSolved = 0
LpStatusOptimal = 1
LpStatusInfeasible = -1
LpStatusUnbounded = -2
LpStatusUndefined = -3
LpStatus = {
    LpStatusNotSolved: "Chưa được giải",
    LpStatusOptimal: "Tối ưu",
    LpStatusInfeasible: "Vô nghiệm",
    LpStatusUnbounded: "Không giới nội",
    LpStatusUndefined: "Không xác định",
}

# solution status
LpSolutionNoSolutionFound = 0
LpSolutionOptimal = 1
LpSolutionIntegerFeasible = 2
LpSolutionInfeasible = -1
LpSolutionUnbounded = -2
LpSolution = {
    LpSolutionNoSolutionFound: "Không tìm thấy lời giải",
    LpSolutionOptimal: "Tìm được nghiệm tối ưu",
    LpSolutionIntegerFeasible: "Tìm được nghiệm",
    LpSolutionInfeasible: "Vô nghiệm",
    LpSolutionUnbounded: "Nghiệm không giới nội",
}
LpStatusToSolution = {
    LpStatusNotSolved: LpSolutionInfeasible,
    LpStatusOptimal: LpSolutionOptimal,
    LpStatusInfeasible: LpSolutionInfeasible,
    LpStatusUnbounded: LpSolutionUnbounded,
    LpStatusUndefined: LpSolutionInfeasible,
}

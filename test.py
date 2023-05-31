import numpy as np
import matplotlib.pyplot as plt

# Define the constraints
x = np.linspace(0, 10, 400)
c11 = 9 - x
c12 = 18 - 3*x
c13 = np.minimum(7, x)
c14 = np.minimum(6, x)

# Plot the constraints
plt.plot(x, c11, label='x1 + x2 <= 9')
plt.plot(x, c12, label='3*x1 + x2 <= 18')
plt.plot(x, c13, label='x1 <= 7')
plt.plot(np.full_like(x, 7), x, label='x1 = 7')
plt.plot(x, c14, label='x2 <= 6')
plt.plot(x, np.full_like(x, 6), label='x2 = 6')

# Shade the feasible region
plt.fill_between(x, np.minimum(c11, np.minimum(c12, np.minimum(c13, 6))), 0, where=(x>=0) & (c11>=0) & (c12>=0) & (c13>=0) & (c14>=0), alpha=0.3)

# Add labels and title
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Feasible Region')

# Add legend
plt.legend()

# Show the plot
plt.show()

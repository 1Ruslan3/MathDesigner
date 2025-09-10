import numpy as np
import matplotlib.pyplot as plt

def snowflake_star(radius=1.0, n_branches=6, inner_ratio=0.6):
    points = []
    step = 2 * np.pi / n_branches
    for i in range(n_branches):
        angle_outer = i * step
        x_outer = radius * np.cos(angle_outer)
        y_outer = radius * np.sin(angle_outer)
        points.append((x_outer, y_outer))
        angle_inner = angle_outer + step / 2
        x_inner = inner_ratio * radius * np.cos(angle_inner)
        y_inner = inner_ratio * radius * np.sin(angle_inner)
        points.append((x_inner, y_inner))

    return np.array(points)

points = snowflake_star(radius=1.0, n_branches=6, inner_ratio=0.5)

plt.figure(figsize=(6, 6))
plt.plot(points[:,0], points[:,1], color="skyblue", linewidth=2)
plt.fill(points[:,0], points[:,1], color="skyblue", alpha=0.3)
plt.gca().set_aspect("equal")
plt.axis("off")
plt.title("Снежинка с острыми углами", fontsize=14)
plt.show()

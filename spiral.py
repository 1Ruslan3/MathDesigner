import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


m = 8
n_circles = 30
scale = 0.35

theta_step = 4 * np.pi / (2 * m + 1)
thetas = np.arange(n_circles) * theta_step

radii = 2 ** (thetas / (2 * np.pi)) * scale

x = radii * np.cos(thetas)
y = radii * np.sin(thetas)

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect("equal")
ax.axis("off")

dots = ax.scatter(x, y, s=300, color="skyblue", alpha=0.7, edgecolor="blue")

def animate(frame):
    angle = np.deg2rad(frame)
    x_rot = x * np.cos(angle) - y * np.sin(angle)
    y_rot = x * np.sin(angle) + y * np.cos(angle)
    dots.set_offsets(np.c_[x_rot, y_rot])
    return dots,

ani = animation.FuncAnimation(fig, animate, frames=360, interval=50, blit=True)

plt.show()

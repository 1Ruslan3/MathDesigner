import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

m = 11
n_circles = 41
scale = 0.85
r0 = 0.1 * scale

dtheta = 2 * np.pi / (m + 0.5)

growth = 2 ** (1.0 / m)

r = np.zeros(n_circles)
rho = np.zeros(n_circles)
theta = np.zeros(n_circles)

r[0] = r0
rho[0] = 0.0
theta[0] = 0.0

for k in range(1, n_circles):
    theta[k] = theta[k-1] + dtheta
    r[k] = r[k-1] * growth
    d = r[k-1] + r[k]
    sin_term = rho[k-1] * np.sin(dtheta)
    cos_term = rho[k-1] * np.cos(dtheta)
    discriminant = d**2 - sin_term**2
    if discriminant < 0:
        print(f"Ошибка: кружки {k-1} и {k} пересекаются (дискриминант отрицательный).")
        break
    rho[k] = cos_term + np.sqrt(discriminant)

x = rho * np.cos(theta)
y = rho * np.sin(theta)

max_extent = np.max(rho + r) + 0.2

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-max_extent, max_extent)
ax.set_ylim(-max_extent, max_extent)
ax.set_aspect("equal")
ax.axis("off")

circles = []
for i in range(n_circles):
    circ = Circle((x[i], y[i]), r[i], color="red", alpha=0.7, ec="black", lw=1)
    ax.add_patch(circ)
    circles.append(circ)

def animate(frame):
    angle = np.deg2rad(frame)
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    for i, circ in enumerate(circles):
        xr = x[i] * cos_a - y[i] * sin_a
        yr = x[i] * sin_a + y[i] * cos_a
        circ.center = (xr, yr)
    return circles

ani = animation.FuncAnimation(fig, animate, frames=240, interval=7~0, blit=True, repeat=True)

plt.show()
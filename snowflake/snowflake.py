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

    points.append(points[0])
    return np.array(points)

def apply_rotation(points, rotation):
    cos_angle = np.cos(rotation)
    sin_angle = np.sin(rotation)

    rotated_points = np.zeros_like(points)
    rotated_points[:, 0] = points[:, 0] * cos_angle - points[:, 1] * sin_angle
    rotated_points[:, 1] = points[:, 0] * sin_angle + points[:, 1] * cos_angle

    return rotated_points


def elegant_snowflakes(n_snowflakes=4, min_radius=0.3, max_radius=1.0,
                       min_branches=5, max_branches=8, rotation_step=np.pi / 6):

    plt.figure(figsize=(8, 8))
    plt.gca().set_facecolor('white')

    radii = np.random.uniform(min_radius, max_radius, n_snowflakes)
    radii = np.sort(radii)[::-1]

    branches_list = np.random.randint(min_branches, max_branches + 1, n_snowflakes)

    for i in range(n_snowflakes):
        radius = radii[i]
        n_branches = branches_list[i]
        rotation = i * rotation_step

        inner_ratio = 0.5

        points = snowflake_star(radius, n_branches, inner_ratio)
        rotated_points = apply_rotation(points, rotation)

        fill_alpha = 0.05 + 0.1 * (radius - min_radius) / (max_radius - min_radius)

        plt.fill(rotated_points[:, 0], rotated_points[:, 1],
                 color='skyblue', alpha=fill_alpha)
        plt.plot(rotated_points[:, 0], rotated_points[:, 1],
                 color='blue', alpha=0.7, linewidth=1.8)

        plt.text(radius + 0.1, 0.1, f'{n_branches}',
                 fontsize=8, alpha=0.5, ha='center')

    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.title(f"Снежинки с разными осями симметрии (n={n_snowflakes})", fontsize=14)
    plt.tight_layout()
    plt.show()

elegant_snowflakes(4, min_branches=6, max_branches=6)

import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import numpy as np
from typing import List, Tuple, Dict
class EllerMazeVisualizer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.maze = None
        self.steps = []
        self.current_step = 0

    def generate_maze(self) -> np.ndarray:
        self.maze = np.ones((self.height * 2 + 1, self.width * 2 + 1), dtype=int)
        self.steps = []

        current_sets = {}
        set_counter = 0
        set_colors = {}

        self._save_step("Инициализация")

        for row in range(self.height):
            for col in range(self.width):
                if row == 0 or col not in current_sets:
                    current_sets[col] = set_counter
                    if set_counter not in set_colors:
                        set_colors[set_counter] = random.random()
                    set_counter += 1

            self._visualize_sets(current_sets, set_colors, f"Строка {row + 1}: Инициализация множеств")

            for col in range(self.width - 1):
                if (current_sets[col] != current_sets[col + 1] and
                        random.random() > 0.4):

                    old_set = current_sets[col + 1]
                    new_set = current_sets[col]

                    for key, value in current_sets.items():
                        if value == old_set:
                            current_sets[key] = new_set

                    maze_col = col * 2 + 1
                    maze_row = row * 2 + 1
                    self.maze[maze_row][maze_col + 1] = 0

                    self._visualize_sets(current_sets, set_colors,
                                         f"Строка {row + 1}: Удаление горизонтальной стены между {col} и {col + 1}")

            new_row_sets = {}
            sets_dict = {}

            for col, set_id in current_sets.items():
                if set_id not in sets_dict:
                    sets_dict[set_id] = []
                sets_dict[set_id].append(col)

            for set_id, columns in sets_dict.items():
                num_connections = random.randint(1, len(columns))
                connections = random.sample(columns, num_connections)

                for col in connections:
                    if row < self.height - 1:
                        maze_col = col * 2 + 1
                        maze_row = row * 2 + 1
                        self.maze[maze_row + 1][maze_col] = 0
                        new_row_sets[col] = set_id

            self._visualize_sets(current_sets, set_colors,
                                 f"Строка {row + 1}: Вертикальные соединения")

            if row < self.height - 1:
                for col in range(self.width):
                    if col not in new_row_sets:
                        new_row_sets[col] = set_counter
                        set_colors[set_counter] = random.random()
                        set_counter += 1

                current_sets = new_row_sets

                self._visualize_sets(current_sets, set_colors,
                                     f"Строка {row + 1}: Переход к следующей строке")

        if self.height > 1:
            last_row = self.height - 1
            for col in range(self.width - 1):
                if current_sets[col] != current_sets[col + 1]:
                    # Объединяем множества
                    old_set = current_sets[col + 1]
                    new_set = current_sets[col]

                    for key, value in current_sets.items():
                        if value == old_set:
                            current_sets[key] = new_set

                    # Убираем стену
                    maze_col = col * 2 + 1
                    maze_row = last_row * 2 + 1
                    self.maze[maze_row][maze_col + 1] = 0

            self._visualize_sets(current_sets, set_colors, "Завершающая строка: Объединение множеств")

        for row in range(self.height):
            for col in range(self.width):
                maze_row = row * 2 + 1
                maze_col = col * 2 + 1
                self.maze[maze_row][maze_col] = 0

        self.maze[1][0] = 0
        self.maze[self.height * 2 - 1][self.width * 2] = 0
        self._save_step("Готовый лабиринт")

        return self.maze

    def _visualize_sets(self, current_sets: Dict, set_colors: Dict, title: str):
        temp_maze = self.maze.copy()

        for col, set_id in current_sets.items():
            row_idx = len(self.steps) // self.width
            maze_row = min(row_idx * 2 + 1, self.height * 2 - 1)
            maze_col = col * 2 + 1

            temp_maze[maze_row][maze_col] = set_id + 2

        self.steps.append((temp_maze.copy(), title))

    def _save_step(self, title: str):
        self.steps.append((self.maze.copy(), title))

    def plot_maze(self, show_solution: bool = False):
        if self.maze is None:
            print("Сначала сгенерируйте лабиринт!")
            return

        fig, ax = plt.subplots(figsize=(12, 8))

        cmap = colors.ListedColormap(['white', 'black'])
        bounds = [0, 0.5, 1]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        ax.imshow(self.maze, cmap=cmap, norm=norm)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Лабиринт, сгенерированный алгоритмом Эллера',
                     fontsize=16, pad=20)

        ax.text(0, 1, 'Вход', ha='center', va='bottom',
                fontsize=12, color='red', weight='bold')
        ax.text(self.width * 2, self.height * 2 - 1, 'Выход',
                ha='center', va='top', fontsize=12, color='green', weight='bold')

        plt.tight_layout()
        plt.show()

    def animate_generation(self, interval: int = 500):
        if not self.steps:
            print("Сначала сгенерируйте лабиринт!")
            return

        fig, ax = plt.subplots(figsize=(12, 8))

        colors_list = ['white', 'black'] + ['lightgray'] * 100
        cmap = colors.ListedColormap(colors_list)

        def animate(frame):
            ax.clear()
            maze_data, title = self.steps[frame]

            vmax = max(2, np.max(maze_data) + 1)
            im = ax.imshow(maze_data, cmap=cmap, vmin=0, vmax=vmax)

            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(f'Генерация лабиринта: {title}\nШаг {frame + 1}/{len(self.steps)}',
                         fontsize=14, pad=20)

            return [im]

        anim = animation.FuncAnimation(
            fig, animate, frames=len(self.steps),
            interval=interval, blit=False, repeat=False
        )

        plt.tight_layout()
        plt.show()

        return anim

    def plot_generation_steps(self, steps_to_show: List[int] = None):
        if not self.steps:
            print("Сначала сгенерируйте лабиринт!")
            return

        if steps_to_show is None:
            total_steps = len(self.steps)
            steps_to_show = [0, total_steps // 4, total_steps // 2,
                             total_steps * 3 // 4, total_steps - 1]

        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()

        colors_list = ['white', 'black'] + ['lightgray'] * 100
        cmap = colors.ListedColormap(colors_list)

        for i, step_idx in enumerate(steps_to_show):
            if i >= len(axes):
                break

            maze_data, title = self.steps[step_idx]
            vmax = max(2, np.max(maze_data) + 1)

            axes[i].imshow(maze_data, cmap=cmap, vmin=0, vmax=vmax)
            axes[i].set_xticks([])
            axes[i].set_yticks([])
            axes[i].set_title(f'Шаг {step_idx + 1}: {title}', fontsize=12)

        for i in range(len(steps_to_show), len(axes)):
            axes[i].set_visible(False)

        plt.tight_layout()
        plt.show()

class MazeSolver:
    @staticmethod
    def solve_maze(maze: np.ndarray) -> np.ndarray:
        height, width = maze.shape

        start = (1, 0)
        end = (height - 2, width - 1)

        queue = [start]
        visited = {start: None}

        while queue:
            current = queue.pop(0)

            if current == end:
                break

            row, col = current
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < height and 0 <= new_col < width and
                        maze[new_row, new_col] == 0 and (new_row, new_col) not in visited):
                    queue.append((new_row, new_col))
                    visited[(new_row, new_col)] = current

        path = []
        current = end
        while current != start:
            path.append(current)
            current = visited[current]
        path.append(start)
        path.reverse()

        return path

if __name__ == "__main__":
    visualizer = EllerMazeVisualizer(10, 10)

    print("Генерация лабиринта...")
    maze = visualizer.generate_maze()

    print("Визуализация готового лабиринта:")
    visualizer.plot_maze()

    print("\nАнимация процесса генерации...")
    visualizer.animate_generation(interval=300)

    print("\nКлючевые этапы генерации:")
    visualizer.plot_generation_steps()

    print("\nЛабиринт с решением:")
    solver = MazeSolver()
    path = solver.solve_maze(maze)

    fig, ax = plt.subplots(figsize=(12, 8))

    maze_with_path = maze.copy()
    for row, col in path:
        maze_with_path[row, col] = 2

    cmap = colors.ListedColormap(['white', 'black', 'red'])
    bounds = [0, 0.5, 1.5, 2.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    ax.imshow(maze_with_path, cmap=cmap, norm=norm)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Лабиринт с решением (красный путь)', fontsize=16, pad=20)

    plt.tight_layout()
    plt.show()
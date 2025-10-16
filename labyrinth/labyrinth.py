import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


class MazeGenerator:
    def __init__(self):
        self.directions = {
            'N': (0, -2),
            'S': (0, 2),
            'E': (2, 0),
            'W': (-2, 0)
        }

    def generate_maze(self, width: int, height: int) -> np.ndarray:
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        maze = np.ones((height, width), dtype=int)

        start_x, start_y = 1, 1
        maze[start_y, start_x] = 0

        stack = [(start_x, start_y)]

        while stack:
            current_x, current_y = stack[-1]

            possible_directions = []

            for direction, (dx, dy) in self.directions.items():
                next_x, next_y = current_x + dx, current_y + dy

                if (0 <= next_x < width and
                        0 <= next_y < height and
                        maze[next_y, next_x] == 1):
                    possible_directions.append((direction, next_x, next_y))

            if possible_directions:
                direction, next_x, next_y = random.choice(possible_directions)
                dx, dy = self.directions[direction]

                wall_x = current_x + dx // 2
                wall_y = current_y + dy // 2
                maze[wall_y, wall_x] = 0

                maze[next_y, next_x] = 0

                stack.append((next_x, next_y))
            else:
                stack.pop()

        maze[1, 0] = 0
        maze[height - 2, width - 1] = 0

        return maze

    def visualize_maze(self, maze: np.ndarray, show_solution: bool = False):
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))

        cmap = ListedColormap(['white', 'black'])

        ax.imshow(maze, cmap=cmap, interpolation='nearest')

        entrance_pos = (0, 1)
        exit_pos = (maze.shape[1] - 1, maze.shape[0] - 2)

        ax.plot(entrance_pos[0], entrance_pos[1], 'gs', markersize=10, label='Вход')
        ax.plot(exit_pos[0], exit_pos[1], 'rs', markersize=10, label='Выход')

        ax.set_title(f'Лабиринт {maze.shape[1]}x{maze.shape[0]}', fontsize=16, fontweight='bold')
        ax.set_xlabel('Ширина')
        ax.set_ylabel('Высота')
        ax.legend(loc='upper right')
        ax.grid(False)

        ax.set_xticks([])
        ax.set_yticks([])

        wall_cells = np.sum(maze == 1)
        path_cells = np.sum(maze == 0)
        total_cells = maze.size

        info_text = f'Общее количество клеток: {total_cells}\nСтены: {wall_cells}\nПроходы: {path_cells}'
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        plt.tight_layout()
        plt.show()

        if show_solution:
            self.show_solution(maze)

    def show_solution(self, maze: np.ndarray):
        solution = self.solve_maze(maze)
        if not solution:
            print("Решение не найдено!")
            return

        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        cmap = ListedColormap(['white', 'black'])

        ax.imshow(maze, cmap=cmap, interpolation='nearest')

        solution_y, solution_x = zip(*solution)
        ax.plot(solution_x, solution_y, 'b-', linewidth=2, alpha=0.7, label='Решение')

        ax.plot(solution_x[0], solution_y[0], 'gs', markersize=10, label='Вход')
        ax.plot(solution_x[-1], solution_y[-1], 'rs', markersize=10, label='Выход')

        ax.set_title('Решение лабиринта', fontsize=16, fontweight='bold')
        ax.legend()
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])

        plt.tight_layout()
        plt.show()

    def solve_maze(self, maze: np.ndarray) -> list:
        start = (1, 0)
        end = (maze.shape[0] - 2, maze.shape[1] - 1)
        visited = set()
        stack = [(start, [start])]

        while stack:
            (y, x), path = stack.pop()

            if (y, x) == end:
                return path

            if (y, x) in visited:
                continue

            visited.add((y, x))

            for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ny, nx = y + dy, x + dx

                if (0 <= ny < maze.shape[0] and
                        0 <= nx < maze.shape[1] and
                        maze[ny, nx] == 0 and
                        (ny, nx) not in visited):
                    stack.append(((ny, nx), path + [(ny, nx)]))

        return None


def main():
    generator = MazeGenerator()

    print("Генератор лабиринтов с визуализацией")
    print("====================================")

    try:
        size_input = input("Введите размер лабиринта (по умолчанию 150, или введите свой размер): ").strip()

        if size_input == "":
            size = 150
        else:
            size = int(size_input)

        if size < 5:
            print("Минимальный размер лабиринта - 5. Установлен размер 5.")
            size = 5
        elif size > 500:
            print("Слишком большой размер! Установлен максимальный размер 500.")
            size = 500

        print(f"Генерация лабиринта размером {size}x{size}...")

        maze = generator.generate_maze(size, size)

        print(f"Лабиринт сгенерирован!")
        print(f"Фактический размер: {maze.shape[1]}x{maze.shape[0]}")

        show_solution = input("\nПоказать решение лабиринта? (y/n): ").strip().lower() == 'y'

        print("Визуализация лабиринта...")
        generator.visualize_maze(maze, show_solution=show_solution)

    except ValueError:
        print("Ошибка: пожалуйста, введите корректное число.")
    except KeyboardInterrupt:
        print("\nГенерация прервана пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
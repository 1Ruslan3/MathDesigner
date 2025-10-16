import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


class EllerMazeGenerator:
    def __init__(self):
        self.sets = {}
        self.set_counter = 0

    def generate_maze(self, width: int, height: int) -> np.ndarray:
        maze = np.ones((height * 2 + 1, width * 2 + 1), dtype=int)

        for row in range(height):
            self._process_row(maze, row, width)

        self._process_final_row(maze, height - 1, width)

        maze[1, 0] = 0
        maze[-2, -1] = 0

        return maze

    def _process_row(self, maze: np.ndarray, row: int, width: int):
        y = row * 2 + 1

        if row == 0:
            self._initialize_first_row(width)
        else:
            self._propagate_sets_from_previous_row(width)

        self._create_vertical_connections(maze, y, width)

        self._create_horizontal_connections(maze, y, width, row)

    def _initialize_first_row(self, width: int):
        self.sets = {}
        self.set_counter = 0
        for x in range(width):
            if x not in self.sets:
                self.set_counter += 1
                self.sets[x] = self.set_counter

    def _propagate_sets_from_previous_row(self, width: int):
        new_sets = {}
        for x in range(width):
            if x in self.sets:
                new_sets[x] = self.sets[x]
            else:
                self.set_counter += 1
                new_sets[x] = self.set_counter
        self.sets = new_sets

    def _create_vertical_connections(self, maze: np.ndarray, y: int, width: int):
        for x in range(width):
            maze_x = x * 2 + 1
            maze[y, maze_x] = 0

    def _create_horizontal_connections(self, maze: np.ndarray, y: int, width: int, row: int):
        maze_y = y

        for x in range(width - 1):
            current_set = self.sets[x]
            next_set = self.sets[x + 1]

            if current_set != next_set and np.random.random() > 0.5:
                self._merge_sets(x, x + 1)
                maze_x = x * 2 + 2
                maze[maze_y, maze_x] = 0

        if row < (maze.shape[0] - 3) // 2:
            sets_with_vertical = set()
            for x in range(width):
                current_set = self.sets[x]

                if current_set not in sets_with_vertical or np.random.random() > 0.7:
                    maze_x = x * 2 + 1
                    maze[maze_y + 1, maze_x] = 0
                    sets_with_vertical.add(current_set)
                else:
                    pass

    def _merge_sets(self, x1: int, x2: int):
        set1 = self.sets[x1]
        set2 = self.sets[x2]

        for x in self.sets:
            if self.sets[x] == set2:
                self.sets[x] = set1

    def _process_final_row(self, maze: np.ndarray, row: int, width: int):
        y = row * 2 + 1

        for x in range(width - 1):
            current_set = self.sets[x]
            next_set = self.sets[x + 1]

            if current_set != next_set:
                self._merge_sets(x, x + 1)
                maze_x = x * 2 + 2
                maze[y, maze_x] = 0

    def visualize_maze(self, maze: np.ndarray, title: str = "Лабиринт 200×50 (Алгоритм Эллера)"):
        fig, ax = plt.subplots(1, 1, figsize=(20, 6))

        cmap = ListedColormap(['white', 'black'])

        ax.imshow(maze, cmap=cmap, interpolation='nearest')

        entrance_pos = (0, 1)  # x, y
        exit_pos = (maze.shape[1] - 1, maze.shape[0] - 2)

        ax.plot(entrance_pos[0], entrance_pos[1], 'gs', markersize=15, label='Вход')
        ax.plot(exit_pos[0], exit_pos[1], 'rs', markersize=15, label='Выход')

        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Ширина')
        ax.set_ylabel('Высота')
        ax.legend(loc='upper right')
        ax.grid(False)

        ax.set_xticks([])
        ax.set_yticks([])

        wall_cells = np.sum(maze == 1)
        path_cells = np.sum(maze == 0)
        total_cells = maze.size

        info_text = f'Размер: {maze.shape[1]}×{maze.shape[0]}\nКлетки: {total_cells}\nСтены: {wall_cells}\nПроходы: {path_cells}'
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        plt.tight_layout()
        plt.show()


def main():
    print("Генератор лабиринтов - Алгоритм Эллера")
    print("======================================")

    width = 200
    height = 50

    print(f"Генерация лабиринта размером {width}×{height} клеток...")
    print("Используется модифицированный алгоритм Эллера")

    generator = EllerMazeGenerator()

    maze = generator.generate_maze(width, height)

    print(f"Лабиринт сгенерирован!")
    print(f"Фактический размер: {maze.shape[1]}×{maze.shape[0]} пикселей")
    print(f"Количество стен: {np.sum(maze == 1)}")
    print(f"Количество проходов: {np.sum(maze == 0)}")

    generator.visualize_maze(maze)


if __name__ == "__main__":
    main()
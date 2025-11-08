import random
from collections import deque

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class EllerStream:
    def __init__(self, width, rng=None):
        self.width = width
        self.current_sets = [0] * width
        self.set_id_counter = 1
        self.sets_dict = {}
        self.rng = rng or random.Random()

    def _assign_new_sets_if_needed(self):
        for x in range(self.width):
            if self.current_sets[x] == 0:
                self.current_sets[x] = self.set_id_counter
                self.sets_dict[self.set_id_counter] = [x]
                self.set_id_counter += 1

    def _horizontal_merges(self, openings_row):
        for x in range(self.width - 1):
            left_set = self.current_sets[x]
            right_set = self.current_sets[x + 1]
            if left_set != right_set and self.rng.choice([True, False]):
                openings_row[2 * x + 2] = 0
                old_id = right_set
                new_id = left_set
                for col in self.sets_dict[old_id]:
                    self.current_sets[col] = new_id
                    self.sets_dict[new_id].append(col)
                del self.sets_dict[old_id]

    def _vertical_openings(self):
        next_sets = [0] * self.width
        next_sets_dict = {}
        vertical_open_cols = []
        for set_id, cols in self.sets_dict.items():
            n = len(cols)
            k = self.rng.randint(1, n) if n > 1 else 1
            down_cols = self.rng.sample(cols, k)
            for x in down_cols:
                next_sets[x] = set_id
                if set_id not in next_sets_dict:
                    next_sets_dict[set_id] = []
                next_sets_dict[set_id].append(x)
            vertical_open_cols.extend(down_cols)
        self.current_sets = next_sets
        self.sets_dict = next_sets_dict
        return vertical_open_cols

    def next_raster_pair(self):
        self._assign_new_sets_if_needed()

        row_width = 2 * self.width + 1
        cell_row = np.ones((row_width,), dtype=np.uint8)
        for x in range(self.width):
            cell_row[2 * x + 1] = 0

        self._horizontal_merges(cell_row)

        wall_row = np.ones((row_width,), dtype=np.uint8)
        open_cols = self._vertical_openings()
        for x in open_cols:
            wall_row[2 * x + 1] = 0

        return cell_row, wall_row


class InfiniteMazeGame:
    def __init__(self, width_cells, window_height_cells, seed=None):
        self.width_cells = width_cells
        self.window_height_cells = window_height_cells
        self.rng = random.Random() if seed is None else random.Random(seed)
        self.stream = EllerStream(width_cells, rng=self.rng)

        self.raster_width = 2 * width_cells + 1
        self.raster_height = 2 * window_height_cells + 1

        self.buffer = deque(maxlen=self.raster_height + 50)

        self.buffer.append(np.ones((self.raster_width,), dtype=np.uint8))

        while len(self.buffer) < self.raster_height:
            cell_row, wall_row = self.stream.next_raster_pair()
            self.buffer.append(cell_row)
            self.buffer.append(wall_row)

        self.player_x = 2 * (self.width_cells // 2) + 1
        self.player_y = 1
        self.score_levels = 0
        self.game_over = False
        self.invulnerable_frames = 15

        self._rows_scrolled = 0

        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_axis_off()
        self.img = None
        self.player_dot = None

    def _ensure_buffer_filled(self):
        while len(self.buffer) < self.raster_height + 2:
            cell_row, wall_row = self.stream.next_raster_pair()
            self.buffer.append(cell_row)
            self.buffer.append(wall_row)

    def _scroll_up_one_pixel_row(self):
        if len(self.buffer) > 0:
            self.buffer.popleft()
        self._rows_scrolled += 1
        if self._rows_scrolled % 2 == 0:
            self.score_levels += 1

        self._ensure_buffer_filled()

    def _current_window_array(self):
        rows = list(self.buffer)[: self.raster_height]
        return np.vstack(rows)

    def _valid_move(self, nx, ny, grid):
        if nx < 0 or nx >= self.raster_width or ny < 0 or ny >= self.raster_height:
            return False
        return grid[ny, nx] == 0

    def on_key(self, event):
        if self.game_over:
            return
        grid = self._current_window_array()
        nx, ny = self.player_x, self.player_y
        if event.key in ['left', 'a']:
            nx -= 1
        elif event.key in ['right', 'd']:
            nx += 1
        elif event.key in ['up', 'w']:
            ny -= 1
        elif event.key in ['down', 's']:
            ny += 1
        if self._valid_move(nx, ny, grid):
            self.player_x, self.player_y = nx, ny
            # Instant visual feedback on key press
            if self.player_dot is not None:
                self.player_dot.set_data([self.player_x], [self.player_y])
                self.fig.canvas.draw_idle()

    def update(self, frame):
        if self.game_over:
            return self.img, self.player_dot

        self._scroll_up_one_pixel_row()

        grid = self._current_window_array()

        if self.invulnerable_frames > 0:
            self.invulnerable_frames -= 1
            self.ax.set_title(f'Уровни: {self.score_levels}', fontsize=12)
        else:
            if grid[self.player_y, self.player_x] == 1:
                self.game_over = True
                self.ax.set_title(f'Игра окончена! Уровни: {self.score_levels}', fontsize=14)
            else:
                self.ax.set_title(f'Уровни: {self.score_levels}', fontsize=12)

        if self.img is None:
            self.img = self.ax.imshow(grid, cmap='gray_r', interpolation='none', animated=True)
        else:
            self.img.set_data(grid)

        if self.player_dot is None:
            self.player_dot = self.ax.plot(self.player_x, self.player_y, 'bo', markersize=6)[0]
        else:
            self.player_dot.set_data([self.player_x], [self.player_y])

        return self.img, self.player_dot

    def run(self):
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.anim = FuncAnimation(self.fig, self.update, interval=800, blit=False)
        plt.show()


def main():
    game = InfiniteMazeGame(width_cells=5, window_height_cells=15)
    game.run()


if __name__ == '__main__':
    main()



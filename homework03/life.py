import copy
import pathlib
import random

from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
            self,
            size: Tuple[int, int],
            randomize: bool = True,
            max_generations: Optional[float] = float('inf')) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for y in range(self.rows):
                for x in range(self.cols):
                    grid[y][x] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighbours = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if 0 <= cell[0] + x < self.rows and 0 <= cell[1] + y < self.cols and (x, y) != (0, 0):
                    neighbours.append(self.curr_generation[cell[0] + x][cell[1] + y])
        return neighbours



    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = copy.deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                n = 0
                for a in self.get_neighbours((i, j)):
                    if a:
                        n += 1
                if new_grid[i][j]:
                    if not 2 <= n <= 3:
                        new_grid[i][j] = 0
                else:
                    if n == 3:
                        new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceed:
            self.prev_generation = self.curr_generation.copy()
            self.curr_generation = self.get_next_generation()
            self.n_generation += 1

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """

        return not self.n_generation < self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return not self.curr_generation == self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        fail = open(filename)
        grid = []
        row = []
        column = 0
        line = len(row)
        for line in fail:
            row = [int(i) for i in line if i in '01']
            grid.append(row)
            column += 1
        game = GameOfLife((column, line), False)
        game.prev_generation = GameOfLife.create_grid(game)
        game.curr_generation = grid
        fail.close()
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename) as file:
            for row in self.curr_generation:
                file.write(''.join([str(x) for x in row]))
                file.write('\n')

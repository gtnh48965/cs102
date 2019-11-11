import pygame
import argparse
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                if self.life.curr_generation[y][x]:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x * self.cell_size + 1, y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))

    def get_cell(self, x: int, y: int):
        chec =[ x//self.cell_size, y //self.cell_size]
        return chec

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        paused = False
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    break
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused
                if event.type == MOUSEBUTTONDOWN:
                    if paused:
                        x, y = self.get_cell(*pygame.mouse.get_pos())
                        self.life.curr_generation[y][x] = abs(self.life.curr_generation[y][x] - 1)

            self.screen.fill(pygame.Color('white'))
            self.draw_lines()
            self.draw_grid()

            # Один шаг
            if paused:
                pass
            else:
                if not self.life.is_max_generations_exceed:
                    self.life.step()
                else:
                    pygame.display.set_caption('Game of Life | Generations limit exceed')
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Console Game of life')
    parser.add_argument('--width', type=int, default=640, help='Screen width, px')
    parser.add_argument('--height', type=int, default=480, help='Screen height, px')
    parser.add_argument('--cell-size', type=int, default=10, help='Cell size, px')
    parser.add_argument('--max-generations', default=float('inf'), type=int, help='Maximum generation count')
    args = parser.parse_args()
    game = GameOfLife((args.height // args.cell_size, args.width // args.cell_size), max_generations=args.max_generations)
    gui = GUI(game, args.cell_size)
    gui.run()
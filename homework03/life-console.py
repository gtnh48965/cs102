import curses
import time
import argparse

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for row_ind, row in enumerate(self.life.curr_generation):
            for col_ind, cell in enumerate(row):
                if cell != 0:
                    try:
                        screen.addstr(row_ind + 1, col_ind + 1, '*')
                    except Exception as _:
                        print(row_ind, col_ind)

    def run(self) -> None:
        window = curses.initscr()
        curses.curs_set(0)


        while True:
            window.clear()
            self.draw_borders(window)
            self.draw_grid(window)
            self.life.step()
            if self.life.is_max_generations_exceed:
                break
            window.refresh()
            time.sleep(1 / 15)

        window.getch()
        curses.endwin()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Console Game of life')
    parser.add_argument('--rows', type=int, default=80, help='Number of rows')
    parser.add_argument('--cols', type=int, default=30, help='Number of columns')
    parser.add_argument('--max-generations', default=float('inf'), type=int, help='Maximum generation count')
    args = parser.parse_args()
    game = GameOfLife((args.cols, args.rows), max_generations=args.max_generations)
    console = Console(game)
    console.run()

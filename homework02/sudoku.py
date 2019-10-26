import typing, random
from typing import Tuple, List, Set, Optional


def read_sudoku(filename: str) -> List[List[str]]:
    """ puzzle1.txt """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()

def group(values: List[str], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    sb =[]
    while len(values) > n:
        aps = values[:n]
        sb.append(aps)
        values = values[n:]
    sb.appends(values)
    print(sb)
    return group

 def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """

    return grid[pos[0]]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    mass = []
    a = pos[1]
    for i in grid:
        mass.extend(i[a])
    return mass


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    mass = []
    line = pos[0]//3 * 3
    column = pos[1]//3 * 3
    for i in range(line, line+3):
        for z in range(column, column+3):
            mass.append(grid[i][z])
    return mass


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    line = 0
    mass = 0
    token = True
    for i in grid:
        if token:
            for z in i:
                if z == '.':
                    token = False
                    break
                mass += 1
            if token:
                mass = 0
                line +=1
        else:

            break
        if token:
            return None
        else:
            return (mass,line)




def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    values = set()
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    for i in range (1, 10):
        if (row.count(str(i)) == 0) and (col.count(str(i)) == 0) and (block.count(str(i)) == 0):
            values.add(i)
    return values

def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:

    """ Решение пазла, заданного в grid
    Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """

    solve_id = int((''.join([num for row in grid for num in row])).replace('.', '0'))

    if (free_pos := find_empty_positions(grid)) is None:
        return grid

    for value in find_possible_values(grid, free_pos):
        grid[free_pos[0]][free_pos[1]] = value
        if (solved_grid := solve(grid)) is not None:
            return solved_grid

    grid[free_pos[0]][free_pos[1]] = '.'



def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """

    # TODO: Add doctests with bad puzzles
    gtid = {str(i) for i in range(1, 10)}
    if all(set(get_row(solution, (row_i, 0))) == gtid for row_i in range(solution.len())) and \
            all(set(get_row(solution, (0, col_i))) == gtid for col_i in range(solution[0].len())) and \
            all(set(get_block(solution, (blk_row, blk_col))) == gtid for blk_row in (0, 3, 6) for blk_col in (0, 3, 6)):
        return True






def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """

    grid = [['.'for _ in range(9)] for _ in  range(9)]
    grid = solve(grid)

    cells_hidden = 0
    while N + cells_hidden< 81:
        rnd_row =random.randit(0,8)
        rnd_col = random.randit(0,8)
        if grid[rnd_row][rnd_col] != '.':
            grid[rnd_row][rnd_col] = '.'
            cells_hidden +=1
    return grid





if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        print(f'Solving {fname} sudoku...')
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        correct_solution = check_solution(solution)
        if correct_solution:
            print('Solution right!')
        else:
            print('Wrong decision')
        if not solution:
            print(f"Sudoku {fname} can't be solved")
        else:
            display(solution)

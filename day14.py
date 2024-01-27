from pathlib import Path
import numpy as np
from more_itertools import unzip, pairwise
from typing import Callable, Optional

Coordinate = tuple[int, int]
Line = list[Coordinate]


def load(path: Path) -> list[Line]:
    def parse_coordinates(text: str) -> Coordinate:
        x, y = text.split(',')
        return int(x), int(y)

    def parse_line(text: str) -> Line:
        all_coordinates = text.split(' -> ')
        return [
            parse_coordinates(coordinates)
            for coordinates in all_coordinates
        ]

    content = path.read_text()
    lines = content.split('\n')
    return [
        parse_line(line)
        for line in lines
    ]


def build_matrix(lines: list[Line]) -> np.ndarray:
    all_rows = []
    all_cols = []
    for line in lines:
        cols, rows = unzip(line)
        all_rows.extend(list(rows))
        all_cols.extend(list(cols))
    matrix = np.chararray((max(all_rows) + 1, max(all_cols) - min(all_cols) + 1), unicode=True)
    matrix[:] = '.'
    convert_fn = lambda x: x - min(all_cols)
    for line in lines:
        for (start_col, start_row), (stop_col, stop_row) in pairwise(line):
            if start_row > stop_row:
                start_row, stop_row = stop_row, start_row
            if start_col > stop_col:
                start_col, stop_col = stop_col, start_col
            matrix[start_row: stop_row + 1, convert_fn(start_col): convert_fn(stop_col) + 1] = '█'

    return matrix, convert_fn


def build_set(lines: list[Line]) -> set[Coordinate]:
    coordinates = set()
    for line in lines:
        for (start_col, start_row), (stop_col, stop_row) in pairwise(line):
            if start_row > stop_row:
                start_row, stop_row = stop_row, start_row
            if start_col > stop_col:
                start_col, stop_col = stop_col, start_col
            if start_row == stop_row:
                coordinates = coordinates | {(start_row, value) for value in range(start_col, stop_col + 1)}
            else:
                coordinates = coordinates | {(value, start_col) for value in range(start_row, stop_row + 1)}
    return coordinates


def simulate(matrix: np.ndarray, convert_col: Callable, origin=(0, 500)) -> int:
    def drop() -> bool:
        def next_position(row, col) -> Optional[tuple[int, int]]:
            if row + 1 >= matrix.shape[0]:
                return None
            if matrix[row + 1, convert_col(col)] == '.':
                return row + 1, col
            if convert_col(col) - 1 < 0:
                return None
            if matrix[row + 1, convert_col(col) - 1] == '.':
                return row + 1, col - 1
            if convert_col(col) + 1 >= matrix.shape[1]:
                return None
            if matrix[row + 1, convert_col(col) + 1] == '.':
                return row + 1, col + 1
            return row, col

        sand_row, sand_col = origin
        going_down = True
        oob = False
        while going_down and not oob:
            result = next_position(sand_row, sand_col)
            if result:
                if (sand_row, sand_col) == result:
                    going_down = False
                else:
                    sand_row, sand_col = result
            else:
                oob = True
        if not going_down:
            matrix[sand_row, convert_col(sand_col)] = 'O'
        return not oob

    counts = 0
    next_ = True
    while next_:
        counts += 1
        next_ = drop()
    return counts - 1


def render_matrix(matrix) -> str:
    lines = []
    for row in range(matrix.shape[0]):
        lines.append("".join(matrix[row, :]))
    return "\n".join(lines)


def simulate_efficient(occupied: set[Coordinate], max_row: int, origin=(0, 500)) -> int:
    def drop(curr_occupied: set[Coordinate]) -> tuple[bool, set[Coordinate]]:
        def next_position(row, col) -> Optional[tuple[int, int]]:
            if row + 1 >= max_row:
                return row, col
            if (row + 1, col) not in curr_occupied:
                return row + 1, col
            if (row + 1, col - 1) not in curr_occupied:
                return row + 1, col - 1
            if (row + 1, col + 1) not in curr_occupied:
                return row + 1, col + 1
            return row, col

        sand_row, sand_col = origin
        stop = False
        going_down = True
        while going_down and not stop:
            result = next_position(sand_row, sand_col)
            if result:
                if (sand_row, sand_col) == result and result == origin:
                    stop = True
                elif (sand_row, sand_col) == result:
                    going_down = False
                else:
                    sand_row, sand_col = result
        if not going_down or stop:
            curr_occupied = curr_occupied | {(sand_row, sand_col)}
        return not stop, curr_occupied

    counts = 0
    next_ = True
    while next_:
        counts += 1
        next_, occupied = drop(occupied)
    return counts, occupied


def debug_set(occupied):
    all_rows = [row for row, _ in occupied]
    all_cols = [col for _, col in occupied]
    matrix = np.chararray((max(all_rows) + 1, max(all_cols) - min(all_cols) + 1), unicode=True)
    matrix[:] = '.'
    for row, col in occupied:
        matrix[row, col - min(all_cols)] = '#'
    return matrix



def main():
    lines = load(Path('data/day14.txt'))
    matrix, convert_col = build_matrix(lines)
    print(render_matrix(matrix))
    print(simulate(matrix, convert_col))
    print(render_matrix(matrix))

    occupied = build_set(lines)
    max_row = max(row for row, _ in occupied)
    # print(simulate_efficient(occupied, max_row))
    n, occupied = simulate_efficient(occupied, max_row + 2)
    print(n)
    print(render_matrix(debug_set(occupied)))


if __name__ == '__main__':
    main()

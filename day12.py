import math
from pathlib import Path
import numpy as np
from astar import AStar


def load(path: Path):
    content = path.read_text()
    lines = content.split('\n')
    return np.array(
        [
            [d for d in line]
            for line in lines
        ]
    )


class HillSolver(AStar):
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix

    def check(self, row: int, col: int, curr_level: str) -> bool:
        max_row, max_col = self.matrix.shape
        if row < 0 or row >= max_row:
            return False
        if col < 0 or col >= max_col:
            return False
        next_level = self.matrix[row, col]
        if next_level == 'E':
            next_level = 'z'
        return ord(next_level) <= ord(curr_level) + 1

    def next_steps(self, curr_row: int, curr_col: int) -> list[tuple[int, int]]:
        directions = []
        curr_level = self.matrix[curr_row, curr_col]
        if self.check(curr_row + 1, curr_col, curr_level):
            directions.append((curr_row + 1, curr_col))
        if self.check(curr_row - 1, curr_col, curr_level):
            directions.append((curr_row - 1, curr_col))
        if self.check(curr_row, curr_col + 1, curr_level):
            directions.append((curr_row, curr_col + 1))
        if self.check(curr_row, curr_col - 1, curr_level):
            directions.append((curr_row, curr_col - 1))
        return directions

    def heuristic_cost_estimate(self, current, goal) -> float:
        (x1, y1) = current
        (x2, y2) = goal
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1, n2) -> float:
        return 1

    def neighbors(self, node):
        row, col = node
        return self.next_steps(row, col)


def shortest_path_fast(matrix: np.ndarray) -> int:
    start_row, start_col = np.argwhere(matrix == 'S')[0]
    end_row, end_col = np.argwhere(matrix == 'E')[0]
    matrix[start_row, start_col] = 'a'
    solver = HillSolver(matrix)
    path = solver.astar((start_row, start_col), (end_row, end_col))
    return len(list(path)) - 1

def all_starts(matrix: np.ndarray) -> int:
    end_row, end_col = np.argwhere(matrix == 'E')[0]
    solver = HillSolver(matrix)
    lens = []
    for start_row, start_col in np.argwhere(matrix == 'a'):
        path = solver.astar((start_row, start_col), (end_row, end_col))
        if path:
            lens.append(len(list(path)) - 1)
    return min(lens)


def main():
    matrix = load(Path('data/day12.txt'))
    print(shortest_path_fast(matrix))
    print(all_starts(matrix))


if __name__ == '__main__':
    main()

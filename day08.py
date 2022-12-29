from pathlib import Path
import numpy as np


def load(path: Path) -> np.ndarray:
    content = path.read_text()
    lines = content.split('\n')
    return np.array(
        [
            [int(d) for d in line]
            for line in lines
        ], dtype=int
    )


def visibles(data: np.array) -> int:
    def check_hl() -> bool:
        return np.all(data[row, :col] < data[row, col])

    def check_hr() -> bool:
        return np.all(data[row, col + 1:] < data[row, col])

    def check_vu() -> bool:
        return np.all(data[row + 1:, col] < data[row, col])

    def check_vd() -> bool:
        return np.all(data[:row, col] < data[row, col])

    mask = np.zeros_like(data, dtype=bool)
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            mask[row, col] = mask[row, col] or check_hl() or check_hr() or check_vu() or check_vd()
    return np.sum(mask)


def best_scenic(data: np.array) -> int:
    def scenic_score() -> int:
        def compute(segment):
            if segment.size == 0:
                return 0
            condition = np.where(segment >= data[row, col])[0]
            if condition.size == 0:
                return len(segment)
            return np.min(condition) + 1

        def left():
            return compute(data[row, :col][::-1])

        def right():
            return compute(data[row, col + 1:])

        def down():
            return compute(data[row + 1:, col])

        def up():
            return compute(data[:row, col][::-1])

        return left() * right() * up() * down()

    scores = np.zeros_like(data, dtype=int)
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            scores[row, col] = scenic_score()
    return np.max(scores)


def main():
    matrix = load(Path('data/day08.txt'))
    print(visibles(matrix))
    print(best_scenic(matrix))


if __name__ == '__main__':
    main()

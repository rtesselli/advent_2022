from pathlib import Path

Coordinate = tuple[int, int]


def load(path: Path) -> list[tuple[str, int]]:
    content = path.read_text()
    lines = content.split('\n')
    return [
        (line.split()[0], int(line.split()[1]))
        for line in lines
    ]


def move_head(position: Coordinate, direction: str) -> Coordinate:
    row, col = position
    match direction:
        case 'R':
            return row, col + 1
        case 'L':
            return row, col - 1
        case 'U':
            return row + 1, col
        case 'D':
            return row - 1, col


def update_piece(head_position: Coordinate, tail_position: Coordinate) -> Coordinate:
    def is_close():
        return abs(head_row - tail_row) <= 1 and abs(head_col - tail_col) <= 1

    head_row, head_col = head_position
    tail_row, tail_col = tail_position
    if is_close():
        return tail_position
    if head_row == tail_row:
        if head_col > tail_col:
            return tail_row, head_col - 1
        return tail_row, head_col + 1
    if head_col == tail_col:
        if head_row > tail_row:
            return head_row - 1, head_col
        return head_row + 1, head_col
    if abs(head_row - tail_row) == abs(head_col - tail_col) == 2:
        if head_row > tail_row and head_col > tail_col:
            return head_row - 1, head_col - 1
        if head_row > tail_row and head_col < tail_col:
            return head_row - 1, head_col + 1
        if head_row < tail_row and head_col > tail_col:
            return head_row + 1, head_col - 1
        return head_row + 1, head_col + 1
    if head_row > tail_row:
        if head_row == tail_row + 2:
            return head_row - 1, head_col
        if head_col > tail_col:
            return head_row, head_col - 1
        return head_row, head_col + 1
    if head_row == tail_row - 2:
        return head_row + 1, head_col
    if head_col > tail_col:
        return head_row, head_col - 1
    return head_row, head_col + 1


def simulate(moves: list[tuple[str, int]]) -> int:
    head = tail = (0, 0)
    tail_positions = set()
    for command, amount in moves:
        for step in range(amount):
            head = move_head(head, command)
            tail = update_piece(head, tail)
            tail_positions.add(tail)
    return len(tail_positions)


def simulate2(moves: list[tuple[str, int]]) -> int:
    positions = [(0, 0)] * 10
    tail_positions = set()
    for command, amount in moves:
        for step in range(amount):
            positions[0] = move_head(positions[0], command)
            for idx in range(1, len(positions)):
                positions[idx] = update_piece(positions[idx - 1], positions[idx])
            tail_positions.add(positions[-1])
    return len(tail_positions)


def main():
    moves = load(Path('data/day09.txt'))
    print(simulate(moves))
    print(simulate2(moves))


if __name__ == '__main__':
    main()

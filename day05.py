from pathlib import Path
from collections import defaultdict
import re


def load(path: Path) -> tuple[defaultdict[int, list[str]], list[tuple[int, int, int]]]:
    def parse_drawing(text: str) -> defaultdict[int, list[str]]:
        def stack_id(position: int) -> int:
            return (position - 1) // 4

        lines = text.split('\n')
        stacks = defaultdict(list)
        for line in lines:
            matches = re.finditer(r'[A-Z]', line)
            for match in matches:
                stacks[stack_id(match.start(0))].append(match.string[match.start(0)])
        return stacks

    def parse_moves(text: str) -> list[tuple[int, int, int]]:
        lines = text.split('\n')
        tuples = []
        for line in lines:
            amount, from_, to = re.findall(r'\d+', line)
            tuples.append((int(amount), int(from_) - 1, int(to) - 1))
        return tuples

    content = path.read_text()
    drawing, moves = content.split('\n\n')
    return parse_drawing(drawing), parse_moves(moves)


def do_move(stacks, amount, from_, to):
    to_move = stacks[from_][:amount]
    stacks[from_] = stacks[from_][amount:]
    stacks[to] = to_move[::-1] + stacks[to]


def do_move2(stacks, amount, from_, to):
    to_move = stacks[from_][:amount]
    stacks[from_] = stacks[from_][amount:]
    stacks[to] = to_move + stacks[to]


def main():
    stacks, moves = load(Path("data/day05.txt"))
    for amount, from_, to in moves:
        do_move(stacks, amount, from_, to)
    print("".join([stacks[idx][0] for idx in range(len(stacks))]))

    stacks, moves = load(Path("data/day05.txt"))
    for amount, from_, to in moves:
        do_move2(stacks, amount, from_, to)
    print("".join([stacks[idx][0] for idx in range(len(stacks))]))


if __name__ == '__main__':
    main()

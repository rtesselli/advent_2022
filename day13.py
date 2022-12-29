from pathlib import Path
from typing import Union, Optional
from functools import cmp_to_key

import more_itertools

Packet = list[Union[int, 'Packet']]


def load(path: Path) -> list[tuple[Packet, Packet]]:
    def parse_pair(text: str) -> tuple[Packet, Packet]:
        up, down = text.split('\n')
        return eval(up), eval(down)

    content = path.read_text()
    pairs = content.split('\n\n')
    return [
        parse_pair(pair)
        for pair in pairs
    ]


def good_pair(pair: tuple[Packet, Packet]) -> Optional[bool]:
    def check_values(value_left: Packet, value_right: Packet) -> Optional[bool]:
        if not value_left and not value_right:
            return None
        if not value_left and value_right:
            return True
        if not value_right and value_left:
            return False
        head_left, *tail_left = value_left
        head_right, *tail_right = value_right
        if type(head_left) is int and type(head_right) is int:
            if head_left < head_right:
                return True
            if head_left > head_right:
                return False
            return check_values(tail_left, tail_right)
        if type(head_left) is list and type(head_right) is list:
            result = check_values(head_left, head_right)
            if result is not None:
                return result
            return check_values(tail_left, tail_right)
        if type(head_left) is int:
            head_left = [head_left]
            return check_values([head_left] + tail_left, value_right)
        if type(head_right) is int:
            head_right = [head_right]
            return check_values(value_left, [head_right] + tail_right)
        return None

    up, down = pair
    return check_values(up, down)


def good_pairs(pairs: list[tuple[Packet, Packet]]) -> int:
    good = list(idx for idx, pair in enumerate(pairs, start=1) if good_pair(pair))
    return sum(good)


def compare(x: Packet, y: Packet) -> int:
    result = good_pairs([(x, y)])
    if result:
        return -1
    if result is None:
        return 0
    return 1


def main():
    pairs = load(Path('data/day13.txt'))
    print(good_pairs(pairs))
    pairs = load(Path('data/day13.txt'))
    left, right = more_itertools.unzip(pairs)
    all_packets = list(left) + list(right)
    all_packets.append([[2]])
    all_packets.append([[6]])
    all_sorted = list(sorted(all_packets, key=cmp_to_key(compare)))
    start = all_sorted.index([[2]]) + 1
    stop = all_sorted.index([[6]]) + 1
    print(start * stop)


if __name__ == '__main__':
    main()

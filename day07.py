from pathlib import Path
from typing import Union, Optional

Tree = dict[str, Union[int, 'Tree']]


def load(path: Path) -> Optional[Tree]:
    def cd(arg: str, curr_position: Optional[Tree]) -> Tree:
        if arg == '/':
            return {}
        if curr_position is None:
            raise ValueError("Tree not defined")
        return curr_position[arg]

    def ls(curr_position: Optional[Tree], curr_lines: list[str]) -> tuple[Tree, list[str]]:
        if curr_position is None:
            raise ValueError("Tree not defined")
        while curr_lines and not curr_lines[0].startswith('$'):
            curr_line = curr_lines[0]
            left, right = curr_line.split(' ')
            if left == 'dir':
                curr_position[right] = {'..': curr_position}
            else:
                curr_position[right] = int(left)
            curr_lines = curr_lines[1:]
        return curr_position, curr_lines

    def root(curr_position: Optional[Tree]) -> Optional[Tree]:
        if not curr_position:
            return curr_position
        has_parent = curr_position.get("..", None)
        if has_parent:
            return root(curr_position['..'])
        return curr_position

    lines = path.read_text().split('\n')
    position = None
    while lines:
        line = lines[0]
        if line.startswith("$"):
            args = line.split(' ')
            command = args[1]
            if command == 'cd':
                position = cd(args[-1], position)
                lines = lines[1:]
            elif command == 'ls':
                position, lines = ls(position, lines[1:])

    return root(position)


def compute_sums(tree: Tree) -> dict[str, int]:
    sizes = {}

    def rec_find(curr_tree: Union[Tree, int], curr_path: str) -> int:
        if not curr_tree:
            return 0
        if type(curr_tree) is int:
            return curr_tree
        sum_ = 0
        for key, value in curr_tree.items():
            if type(value) is int:
                sum_ += value
            elif key != '..':
                sub_path = f"{curr_path}/{key}"
                sub_value = rec_find(curr_tree[key], sub_path)
                sum_ += sub_value
                sizes[sub_path] = sub_value
        return sum_

    total = rec_find(tree, '')
    sizes['/'] = total
    return sizes


def main():
    fs = load(Path('data/day07.txt'))
    sums = compute_sums(fs)
    print(sum(value for value in sums.values() if value <= 100000))
    max_capacity = 70000000
    required_space = 30000000
    unused_space = max_capacity - sums['/']
    to_free = required_space - unused_space
    print(min(value for value in sums.values() if value >= to_free))


if __name__ == '__main__':
    main()

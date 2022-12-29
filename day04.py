from pathlib import Path


def load(path: Path) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    def parse(text: str) -> tuple[tuple[int, int], tuple[int, int]]:
        def pair(values: list[text]) -> tuple[int, int]:
            left, right = tuple(int(value) for value in values)
            return left, right

        first, second = text.split(',')
        return pair(first.split('-')), pair(second.split('-'))

    content = path.read_text()
    lines = content.split('\n')
    return [parse(line) for line in lines]


def expand(value: tuple[int, int]) -> set[int]:
    first, second = value
    return set(range(first, second + 1))


def check(elements: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    left, right = elements
    left = expand(left)
    right = expand(right)
    return left & right == left or left & right == right


def check2(elements: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    left, right = elements
    left = expand(left)
    right = expand(right)
    return bool(left & right)


def main():
    lines = load(Path("data/day04.txt"))
    print(sum(check(line) for line in lines))
    print(sum(check2(line) for line in lines))


if __name__ == '__main__':
    main()

from pathlib import Path
from more_itertools import sliced


def load(path: Path) -> list[str]:
    content = path.read_text()
    return content.split('\n')


def find_common(text: str) -> str:
    first, second = text[:len(text) // 2], text[len(text) // 2:]
    return (set(first) & set(second)).pop()


def priority(text: str) -> int:
    if text.islower():
        return ord(text) - 96
    return ord(text) - 38


def find_common_in_group(group: list[str]) -> str:
    first, second, third = group
    return (set(first) & set(second) & set(third)).pop()


def main():
    lines = load(Path('data/day03.txt'))
    score = 0
    for line in lines:
        score += priority(find_common(line))
    print(score)
    score = 0
    for group in sliced(lines, 3):
        score += priority(find_common_in_group(list(group)))
    print(score)


if __name__ == '__main__':
    main()

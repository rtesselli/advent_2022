from pathlib import Path


def load(path: Path) -> list[list[int]]:
    content = path.read_text()
    return [[int(value) for value in bag.split('\n')] for bag in content.split("\n\n")]


def main():
    bags = load(Path('data/day01.txt'))
    sums = list(map(sum, bags))
    print(max(sums))
    print(sum(sorted(sums)[-3:]))


if __name__ == '__main__':
    main()

from pathlib import Path
from more_itertools import windowed


def load(path: Path) -> str:
    return path.read_text().strip()


def find(text: str, window_size: int) -> int:
    for idx, window in enumerate(windowed(text, window_size)):
        if len(set(window)) == window_size:
            return idx + window_size


def main():
    line = load(Path('data/day06.txt'))
    print(find(line, 4))
    print(find(line, 14))


if __name__ == '__main__':
    main()

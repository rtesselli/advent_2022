from pathlib import Path


def load(path: Path) -> list[str]:
    content = path.read_text()
    return content.split('\n')


def signal_strengths(commands: list[str]) -> list[int]:
    def init_sprite(position: int) -> list[str]:
        line = [' '] * 40
        if 0 <= position < len(line):
            line[position] = '█'
        if 0 <= position - 1 < len(line):
            line[position - 1] = '█'
        if 0 <= position + 1 < len(line):
            line[position + 1] = '█'
        return line

    def step(cycle, last_check):
        cycle += 1
        print(sprite[(cycle - 1) % 40], end='')
        if cycle == last_check + 40 or cycle == 20:
            signals.append(register * cycle)
            last_check = cycle
        if cycle % 40 == 0:
            print()
        return cycle, last_check

    register = 1
    current_cycle = 0
    last_cycle_check = 0
    signals = []
    sprite = init_sprite(register)
    for command in commands:
        if command.startswith('noop'):
            current_cycle, last_cycle_check = step(current_cycle, last_cycle_check)
        else:
            current_cycle, last_cycle_check = step(current_cycle, last_cycle_check)
            current_cycle, last_cycle_check = step(current_cycle, last_cycle_check)
            register += int(command.split(' ')[-1])
            sprite = init_sprite(register)
    return signals


def main():
    commands = load(Path('data/day10.txt'))
    signals = signal_strengths(commands)
    print()
    print(sum(signals))


if __name__ == '__main__':
    main()

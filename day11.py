import math
from pathlib import Path
import re
import operator


class Monkey:
    OPERATOR_MAP = {
        '+': operator.add,
        '*': operator.mul
    }

    SELF_OPERATOR_MAP = {
        '+': lambda x: 2 * x,
        '*': lambda x: x ** 2
    }

    def __init__(self, starting_items, update_fn, divisor, true_monkey_id, false_monkey_id):
        self.items = starting_items
        self.update_fn = update_fn
        self.divisor = divisor
        self.true_monkey_id = true_monkey_id
        self.false_monkey_id = false_monkey_id
        self.inspect_counter = 0
        self.modulo = None

    @classmethod
    def from_text(cls, text: str):
        lines = text.split('\n')
        starting_items = list(int(value) for value in re.findall(r"\d+", lines[1]))
        operation = re.findall(r"[+|*]", lines[2])[0]
        update_value = re.findall(r"\d+", lines[2]) or 'old'
        if update_value != 'old':
            update_fn = lambda x: Monkey.OPERATOR_MAP[operation](x, int(update_value[0]))
        else:
            update_fn = Monkey.SELF_OPERATOR_MAP[operation]
        divisor = int(re.findall(r"\d+", lines[3])[0])
        true_monkey_id = int(re.findall(r"\d+", lines[4])[0])
        false_monkey_id = int(re.findall(r"\d+", lines[5])[0])
        return Monkey(starting_items, update_fn, divisor,
                      true_monkey_id, false_monkey_id)

    def inspect_item(self, item_id, divide_condition=True):
        self.inspect_counter += 1
        if not divide_condition:
            self.items[item_id] = self.items[item_id] % self.modulo
        self.items[item_id] = self.update_fn(self.items[item_id])
        if divide_condition:
            self.items[item_id] = int(math.floor(self.items[item_id] / 3))
        else:
            self.items[item_id] = self.items[item_id] % self.modulo
        if self.items[item_id] % self.divisor == 0:
            return self.true_monkey_id
        return self.false_monkey_id

    def throw(self, item_id, other_monkey):
        other_monkey.items.append(self.items.pop(item_id))


def load(path: Path) -> list[Monkey]:
    content = path.read_text()
    blocks = content.split('\n\n')
    return [
        Monkey.from_text(block)
        for block in blocks
    ]


def main():
    monkeys = load(Path('data/day11.txt'))
    for _ in range(20):
        for monkey in monkeys:
            for item_id in range(len(monkey.items)):
                receiver_monkey_id = monkey.inspect_item(0)
                monkey.throw(0, monkeys[receiver_monkey_id])
    top_monkeys = sorted(monkeys, key=lambda x: x.inspect_counter)[-2:]
    print(math.prod(value.inspect_counter for value in top_monkeys))

    monkeys = load(Path('data/day11.txt'))
    mcm = math.prod(monkey.divisor for monkey in monkeys)
    for monkey in monkeys:
        monkey.modulo = mcm
    for round_ in range(1, 10001):
        for idx, monkey in enumerate(monkeys):
            for _ in range(len(monkey.items)):
                receiver_monkey_id = monkey.inspect_item(0, False)
                monkey.throw(0, monkeys[receiver_monkey_id])
    top_monkeys = sorted(monkeys, key=lambda x: x.inspect_counter)[-2:]
    print(math.prod(value.inspect_counter for value in top_monkeys))


if __name__ == '__main__':
    main()

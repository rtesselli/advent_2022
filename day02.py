from typing import Optional
from pathlib import Path
from enum import Enum, auto


class Outcome(Enum):
    LOSE = auto()
    DRAW = auto()
    WIN = auto()


def item(value: str) -> Optional[str]:
    if value in {'A', 'X'}:
        return "rock"
    if value in {'B', 'Y'}:
        return "paper"
    if value in {'C', 'Z'}:
        return "scissors"


def item_score(item_: str) -> Optional[int]:
    if item_ == "rock":
        return 1
    if item_ == "paper":
        return 2
    if item_ == "scissors":
        return 3


def outcome(item_a, item_b: str) -> Outcome:
    if item_a == item_b:
        return Outcome.DRAW
    if item_a == "rock":
        if item_b == "paper":
            return Outcome.WIN
        if item_b == "scissors":
            return Outcome.LOSE
    if item_a == "paper":
        if item_b == "rock":
            return Outcome.LOSE
        if item_b == "scissors":
            return Outcome.WIN
    if item_a == "scissors":
        if item_b == "rock":
            return Outcome.WIN
        if item_b == "paper":
            return Outcome.LOSE


def game_score(value: Outcome) -> int:
    if value == value.LOSE:
        return 0
    if value == value.DRAW:
        return 3
    return 6


def outcome_from_value(value: str) -> Outcome:
    if value == "X":
        return Outcome.LOSE
    if value == "Y":
        return Outcome.DRAW
    return Outcome.WIN


def good_choice(item_: str, outcome_value: Outcome) -> str:
    if outcome_value == Outcome.DRAW:
        return item_
    if outcome_value == Outcome.LOSE:
        if item_ == 'rock':
            return "scissors"
        if item_ == 'paper':
            return "rock"
        if item_ == 'scissors':
            return "paper"
    if outcome_value == Outcome.WIN:
        if item_ == 'rock':
            return "paper"
        if item_ == 'paper':
            return "scissors"
        if item_ == 'scissors':
            return "rock"


def load(path: Path) -> list[tuple[str]]:
    content = path.read_text()
    lines = content.split('\n')
    return [tuple(line.split(' ')) for line in lines]


def main():
    games = load(Path('data/day02.txt'))
    total_score = 0
    total_score2 = 0
    for value_left, value_right in games:
        total_score += game_score(outcome(item(value_left), item(value_right))) + item_score(item(value_right))
        total_score2 += game_score(outcome_from_value(value_right)) + item_score(
            good_choice(item(value_left), outcome_from_value(value_right)))
    print(total_score)
    print(total_score2)


if __name__ == '__main__':
    main()

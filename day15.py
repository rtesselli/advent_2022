from pathlib import Path
import re
from more_itertools import unzip
from itertools import product
from tqdm import tqdm

Coordinate = tuple[int, int]
Interval = tuple[int, int]


def load(path: Path) -> list[tuple[Coordinate, Coordinate]]:
    content = path.read_text()
    lines = content.split('\n')
    out = []
    for line in lines:
        values = re.findall('-?\d+', line)
        out.append(((int(values[1]), int(values[0])), (int(values[3]), int(values[2]))))
    return out


def distance(x: Coordinate, y: Coordinate) -> int:
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def intervals_intersect(first: tuple[int, int], second: tuple[int, int]) -> bool:
    first_start, first_stop = first
    second_start, second_stop = second
    return (
            first_start <= second_start <= first_stop or
            second_start <= first_start <= second_stop or
            second_start <= first_stop <= second_stop or
            first_start <= second_stop <= first_stop
    )


def cross(sensor: Coordinate, ray: int, line: int) -> bool:
    row, col = sensor
    return abs(row - line) <= ray


def track_interval(sensor: Coordinate, row_distance: int, max_ray: int) -> Interval:
    x, y = sensor
    d = abs(max_ray - row_distance)
    return y - d, y + d


def merge(values: list[Interval]) -> list[Interval]:
    changed = True
    curr_values = set(values)
    while changed and len(curr_values) > 1:
        news = set()
        to_remove = set()
        for left, right in product(curr_values, curr_values):
            if left != right and intervals_intersect(left, right):
                new = (min(left[0], right[0]), max(left[1], right[1]))
                if new not in curr_values:
                    news.add((min(left[0], right[0]), max(left[1], right[1])))
                    to_remove.add(left)
                    to_remove.add(right)
                elif new == left:
                    to_remove.add(right)
                elif new == right:
                    to_remove.add(left)
        changed = len(news) > 0
        curr_values = curr_values.union(news).difference(to_remove)
    return list(curr_values)


def project(sensors: list[Coordinate], beacons: list[Coordinate], line: int) -> list[Interval]:
    occupied = []
    for sensor, beacon in zip(sensors, beacons):
        ray = distance(sensor, beacon)
        if cross(sensor, ray, line):
            interval = track_interval(sensor, abs(line - sensor[0]), ray)
            occupied.append(interval)
    return merge(occupied)


def remove_beacons(intervals: list[Interval], beacons: list[Coordinate], line: int) -> set[int]:
    occupied = set()
    for start, stop in intervals:
        occupied = occupied.union(set(range(start, stop + 1)))
    for beacon in beacons:
        row, col = beacon
        if row == line and col in occupied:
            occupied.remove(col)
    return occupied


def add_beacons(intervals: list[Interval], beacons: list[Coordinate], line: int) -> list[Interval]:
    for beacon in beacons:
        row, col = beacon
        if row == line:
            intervals.append((col, col))
    return merge(intervals)


def main():
    lines = load(Path('data/day15.txt'))
    sensors, beacons = unzip(lines)
    sensors = list(sensors)
    beacons = list(beacons)
    print(len(remove_beacons(project(sensors, beacons, 2000000), beacons, 2000000)))

    for line in tqdm(range(0, 4000000 + 1)):
        result = add_beacons(project(sensors, beacons, line), beacons, line)
        if len(result) > 1:
            print((result[0][1] + 1) * 4000000 + line)
            return


if __name__ == '__main__':
    main()

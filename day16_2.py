"""
Day 16: Proboscidea Volcanium
"""

import heapq
import math
import re
from collections import defaultdict
from dataclasses import dataclass

PATTERN = re.compile(
    r"Valve (\w+) has flow rate=(\d+); "
    r"(?:tunnel leads to valve|tunnels lead to valves) (\w+(?:, \w+)*)"
)

SAMPLE_INPUT = [
    "Valve TM has flow rate=0; tunnels lead to valves KF, AA",
    "Valve LG has flow rate=8; tunnels lead to valves DD, UA",
    "Valve IZ has flow rate=20; tunnels lead to valves LY, XC",
    "Valve XF has flow rate=0; tunnels lead to valves PB, QD",
    "Valve FE has flow rate=0; tunnels lead to valves ZW, KF",
    "Valve ZP has flow rate=0; tunnels lead to valves MT, AI",
    "Valve CL has flow rate=0; tunnels lead to valves JN, AI",
    "Valve UA has flow rate=0; tunnels lead to valves VW, LG",
    "Valve VP has flow rate=0; tunnels lead to valves MB, GU",
    "Valve KY has flow rate=0; tunnels lead to valves BZ, CJ",
    "Valve AI has flow rate=11; tunnels lead to valves TL, GG, CL, ZP, MM",
    "Valve GD has flow rate=0; tunnels lead to valves KB, QK",
    "Valve GU has flow rate=14; tunnels lead to valves ZK, VP",
    "Valve RO has flow rate=0; tunnels lead to valves KS, TJ",
    "Valve VW has flow rate=0; tunnels lead to valves UA, KS",
    "Valve YE has flow rate=24; tunnel leads to valve DP",
    "Valve AA has flow rate=0; tunnels lead to valves TL, ZU, TM, RL, BZ",
    "Valve RL has flow rate=0; tunnels lead to valves AA, NU",
    "Valve RG has flow rate=0; tunnels lead to valves CJ, KS",
    "Valve ZW has flow rate=0; tunnels lead to valves TJ, FE",
    "Valve OY has flow rate=0; tunnels lead to valves KS, AO",
    "Valve CE has flow rate=0; tunnels lead to valves QK, IQ",
    "Valve JN has flow rate=0; tunnels lead to valves EK, CL",
    "Valve OF has flow rate=0; tunnels lead to valves KS, ZK",
    "Valve LY has flow rate=0; tunnels lead to valves IZ, EJ",
    "Valve DD has flow rate=0; tunnels lead to valves KF, LG",
    "Valve QK has flow rate=15; tunnels lead to valves CE, EJ, UK, GD",
    "Valve XC has flow rate=0; tunnels lead to valves RA, IZ",
    "Valve EK has flow rate=22; tunnel leads to valve JN",
    "Valve JM has flow rate=0; tunnels lead to valves VF, KF",
    "Valve UK has flow rate=0; tunnels lead to valves PB, QK",
    "Valve ZK has flow rate=0; tunnels lead to valves GU, OF",
    "Valve EJ has flow rate=0; tunnels lead to valves LY, QK",
    "Valve CJ has flow rate=10; tunnels lead to valves WS, IQ, RG, KY",
    "Valve MB has flow rate=18; tunnel leads to valve VP",
    "Valve TL has flow rate=0; tunnels lead to valves AA, AI",
    "Valve KS has flow rate=13; tunnels lead to valves OF, OY, RO, RG, VW",
    "Valve QD has flow rate=0; tunnels lead to valves XF, TJ",
    "Valve CU has flow rate=19; tunnels lead to valves AO, DP",
    "Valve PB has flow rate=5; tunnels lead to valves ZU, GG, XF, UK, VF",
    "Valve KF has flow rate=7; tunnels lead to valves DD, JM, ZH, FE, TM",
    "Valve TJ has flow rate=3; tunnels lead to valves QD, ZW, NU, RO, MT",
    "Valve ZH has flow rate=0; tunnels lead to valves KF, WS",
    "Valve BZ has flow rate=0; tunnels lead to valves KY, AA",
    "Valve NU has flow rate=0; tunnels lead to valves RL, TJ",
    "Valve KB has flow rate=21; tunnels lead to valves RA, GD, JW",
    "Valve WS has flow rate=0; tunnels lead to valves ZH, CJ",
    "Valve ZU has flow rate=0; tunnels lead to valves PB, AA",
    "Valve MT has flow rate=0; tunnels lead to valves ZP, TJ",
    "Valve JW has flow rate=0; tunnels lead to valves MM, KB",
    "Valve DP has flow rate=0; tunnels lead to valves CU, YE",
    "Valve AO has flow rate=0; tunnels lead to valves OY, CU",
    "Valve RA has flow rate=0; tunnels lead to valves KB, XC",
    "Valve VF has flow rate=0; tunnels lead to valves PB, JM",
    "Valve IQ has flow rate=0; tunnels lead to valves CE, CJ",
    "Valve GG has flow rate=0; tunnels lead to valves AI, PB",
    "Valve MM has flow rate=0; tunnels lead to valves AI, JW",
]


def _parse(lines):
    return {
        (match := re.match(PATTERN, line)).group(1): (
            int(match.group(2)),
            match.group(3).split(", "),
        )
        for line in lines
    }


def _distances(adj):
    keys, distances = set(), defaultdict(lambda: math.inf)
    for src, dsts in adj:
        keys.add(src)
        distances[src, src] = 0
        for dst, weight in dsts:
            keys.add(dst)
            distances[dst, dst] = 0
            distances[src, dst] = weight
    for mid in keys:
        for src in keys:
            for dst in keys:
                distance = distances[src, mid] + distances[mid, dst]
                if distance < distances[src, dst]:
                    distances[src, dst] = distance
    return distances


@dataclass(order=True, frozen=True)
class _State:
    rooms: tuple[tuple[str, int]]
    valves: frozenset[str]
    flow: int
    total: int
    time: int


def _solve(lines, num_agents, total_time):
    # pylint: disable=too-many-branches,too-many-nested-blocks,too-many-locals
    graph = _parse(lines)
    distances = _distances(
        (src, ((dst, 1) for dst in dsts)) for src, (_, dsts) in graph.items()
    )
    seen, max_seen = set(), 0
    heap = [
        (
            0,
            _State(
                rooms=(("AA", 0),) * num_agents,
                valves=frozenset(src for src, (flow, _) in graph.items() if flow > 0),
                flow=0,
                total=0,
                time=total_time,
            ),
        )
    ]

    while heap:
        estimate, state = heapq.heappop(heap)
        estimate = -estimate
        if state in seen:
            continue
        seen.add(state)
        potential = estimate + sum(
            max(
                (
                    graph[valve][0] * (state.time - delta - 1)
                    for room, age in state.rooms
                    if (delta := distances[room, valve] - age) in range(state.time)
                ),
                default=0,
            )
            for valve in state.valves
        )
        if estimate > max_seen:
            max_seen = estimate
        if potential < max_seen:
            continue

        moves_by_time = defaultdict(lambda: defaultdict(list))
        for valve in state.valves:
            for i, (room, age) in enumerate(state.rooms):
                delta = distances[room, valve] - age
                if delta in range(state.time):
                    moves_by_time[delta][i].append(valve)
        if not moves_by_time:
            continue

        for delta, moves_by_agent in moves_by_time.items():
            indices = [None] * num_agents
            while True:
                for i, index in enumerate(indices):
                    index = 0 if index is None else index + 1
                    if index < len(moves_by_agent[i]):
                        indices[i] = index
                        break
                    indices[i] = None
                else:
                    break
                valves = [
                    (i, moves_by_agent[i][index])
                    for i, index in enumerate(indices)
                    if index is not None
                ]
                if len(valves) != len(set(valve for _, valve in valves)):
                    continue
                new_rooms = [(room, age + delta + 1) for room, age in state.rooms]
                for i, valve in valves:
                    new_rooms[i] = valve, 0
                rate = sum(graph[valve][0] for _, valve in valves)
                new_state = _State(
                    rooms=tuple(sorted(new_rooms)),
                    valves=state.valves - set(valve for _, valve in valves),
                    flow=state.flow + rate,
                    total=state.total + state.flow * (delta + 1),
                    time=state.time - delta - 1,
                )
                heapq.heappush(heap, (-estimate - rate * new_state.time, new_state))

    return max_seen


def part1(lines):
    """
    >>> part1(SAMPLE_INPUT)
    1651
    """
    return _solve(lines, num_agents=1, total_time=30)


def part2(lines):
    """
    >>> part2(SAMPLE_INPUT)
    1707
    """
    return _solve(lines, num_agents=2, total_time=26)


if __name__ == '__main__':
    parts = (part1, part2)
    print(part1(SAMPLE_INPUT))

from pathlib import Path
from functools import cache
import re
import dijkstar

Graph = dict[str, dict[str, int | list[str]]]


def load(path: Path) -> Graph:
    content = path.read_text()
    lines = content.split('\n')
    graph = {}
    for line in lines:
        flow_rate = re.findall(r"\d+", line)
        keys = re.findall(r"[A-Z]{2}", line)
        key, *neighbors = keys
        graph[str(key)] = {
            'flow_rate': int(flow_rate[0]),
            'neighbors': list(str(neighbor) for neighbor in neighbors)
        }
    return graph


def to_dijkstra_graph(graph: Graph) -> dijkstar.Graph:
    out = dijkstar.Graph()
    for node, values in graph.items():
        for neighbor in values["neighbors"]:
            out.add_edge(node, neighbor, 1)
    return out


def all_distances(graph: dijkstar.Graph) -> dict[tuple[str, str], int]:
    distances = {}
    for node_a in graph.keys():
        for node_b in graph.keys():
            shortest_path = dijkstar.algorithm.find_path(graph, node_a, node_b)
            distances[(node_a, node_b)] = shortest_path.total_cost
    return distances


def solve(graph: Graph, distances: dict[tuple[str, str], int]) -> int:
    positive_flow = {node for node in graph.keys() if graph[node]["flow_rate"] > 0}

    @cache
    def estimate(action: str, mins_left: int, opened: frozenset[str]) -> int:
        distances_from_action = {to: distance for (from_, to), distance in distances.items() if from_ == action}
        openables = {to: distance for to, distance in distances_from_action.items() if
                     to not in opened and graph[to]['flow_rate'] > 0}
        reachables = {to: distance for to, distance in openables.items() if distance <= mins_left}
        return sum((mins_left - distance) * graph[to]["flow_rate"] for to, distance in reachables.items())

    @cache
    def rec_solve(node: str, mins_left: int, opened: frozenset[str], previous_node: str) -> tuple[int, list[str]]:
        data = graph[node]
        if mins_left == 0:
            return 0, [previous_node, node]
        curr_score = 0
        if node == previous_node:
            curr_score += mins_left * data["flow_rate"]
            opened = opened | {node}
        if not positive_flow - opened:
            return curr_score, [previous_node, node]
        actions = [neighbor for neighbor in data['neighbors'] if neighbor != previous_node]
        if data["flow_rate"] > 0 and node not in opened:
            actions.append(node)
        estimated_actions = [(action, estimate(action, mins_left - 1, opened)) for action in actions]
        best_score = -1
        best_path = []
        for action, max_estimate in sorted(estimated_actions, key=lambda x: x[1], reverse=True):
            if best_score < max_estimate and max_estimate > 0:
                score, path = rec_solve(action, mins_left - 1, frozenset(opened), node)
                if score > best_score:
                    best_score = score
                    best_path = path
        if best_score > -1:
            return best_score + curr_score, [previous_node] + best_path
        return curr_score, [previous_node, node]

    start = list(graph.keys())[0]
    return rec_solve(start, 30, frozenset(), '')


def main():
    graph = load(Path('data/day16.txt'))
    dijkstra_graph = to_dijkstra_graph(graph)
    distances = all_distances(dijkstra_graph)
    print(solve(graph, distances))

#            11 * 26 + 21 * 22 + 15 * 19 + 10 * 15 + 13 * 12 + 19 * 8 + 24 * 5
#               11 * 27 + 21 * 23 + 15 * 20 + 10 * 16 + 13 * 13 + 19 * 9 + 24 * 6
#            20 * 28 + 13 * 25 + 21 * 21 + 22 * 13 + 3 * 9 + 2 * 6
    # path = ['AA', 'DD', 'DD', 'AA', 'BB', 'BB', 'AA', 'II', 'JJ', 'JJ', 'II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG', 'FF', 'EE', 'EE', 'DD', 'CC', 'CC']
    # path = ['TM', 'AA', 'TL', 'AI', 'AI', 'MM', 'JW', 'KB', 'KB', 'GD', 'QK', 'QK', 'CE', 'IQ', 'CJ', 'CJ', 'RG', 'KS', 'KS', 'OY', 'AO', 'CU', 'CU', 'DP', 'YE', 'YE']
    # mins = 31
    # score = 0
    # for idx in range(1, len(path)):
    #     if path[idx] == path[idx - 1]:
    #         score += graph[path[idx]]['flow_rate'] * (mins-1)
    #     mins -= 1
    # print(score)


if __name__ == '__main__':
    main()

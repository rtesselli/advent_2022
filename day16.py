from pathlib import Path
from typing import Optional
import re
import dijkstar

Graph = dict[str, dict[str, int | list[str]]]


# Tree = dict[str, int | str | list['Tree']]


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


# def solve(graph: Graph) -> int:
#     def indent(remaining_time: int) -> str:
#         return " " * (30 - remaining_time)
#
#     def rec_solve(curr_node: str, opened: set[str], remaining_time: int, score: int,
#                   previous_node: Optional[str] = None) -> int:
#         # print(f"{indent(remaining_time)}I'm in {curr_node}, remaining time: {remaining_time}")
#         if remaining_time == 0:
#             # print(f"{indent(remaining_time)}Finished, score: {score}")
#             return score
#         scores = []
#         openable = graph[curr_node]['flow_rate'] > 0 and curr_node not in opened
#         if openable:
#             # print(f"{indent(remaining_time)}Opening valve")
#             scores.append(
#                 rec_solve(
#                     curr_node,
#                     opened | {curr_node},
#                     remaining_time - 1,
#                     score + graph[curr_node]['flow_rate'] * (remaining_time - 1),
#                     None
#                 )
#             )
#         for neighbor in graph[curr_node]['neighbors']:
#             if neighbor != previous_node:
#                 # print(f"{indent(remaining_time)}Going to {neighbor}")
#                 scores.append(
#                     rec_solve(
#                         neighbor,
#                         opened,
#                         remaining_time - 1,
#                         score,
#                         curr_node
#                     )
#                 )
#         if scores:
#             return max(scores)
#         # print(f"{indent(remaining_time)}Nothing to do, score: {score}")
#         return score
#
#     return rec_solve(list(graph.keys())[0], set(), 30, 0)
#
#
# def to_tree(graph: Graph) -> Tree:
#     def rec_to_tree(curr_node: str, visited: set[str]) -> Tree:
#         to_visit = set(graph[curr_node]["neighbors"]) - visited
#         if not to_visit:
#             return {
#                 'name': curr_node,
#                 'flow_rate': graph[curr_node]["flow_rate"],
#                 'children': []
#             }
#         children = []
#         for node in to_visit:
#             children.append(rec_to_tree(node, visited | {curr_node}))
#         return {
#             'name': curr_node,
#             'flow_rate': graph[curr_node]["flow_rate"],
#             'children': children
#         }
#
#     start = list(graph.keys())[0]
#     return rec_to_tree(start, set())


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

from collections import Counter

# c = Counter()

def solve(graph: Graph, distances: dict[tuple[str, str], int]) -> int:
    positive_flow = {node for node in graph.keys() if graph[node]["flow_rate"] > 0}

    def estimate(action: str, mins_left: int, opened: set[str] | frozenset[str]) -> int:
        distances_from_action = {to: distance for (from_, to), distance in distances.items() if from_ == action}
        openables = {to: distance for to, distance in distances_from_action.items() if
                     to not in opened and graph[to]['flow_rate'] > 0}
        reachables = {to: distance for to, distance in openables.items() if distance <= mins_left}
        return sum((mins_left - distance) * graph[to]["flow_rate"] for to, distance in reachables.items())

    def rec_solve(node: str, mins_left: int, curr_score: int, opened: frozenset[str], previous_node: Optional[str]) -> int:
        data = graph[node]
        if mins_left == 0:
            return curr_score
        if node == previous_node:
            curr_score += mins_left * data["flow_rate"]
            opened = opened | {node}
        if not positive_flow - opened:
            return curr_score
        actions = [neighbor for neighbor in data['neighbors'] if neighbor != previous_node]
        if data["flow_rate"] > 0 and node not in opened:
            actions.append(node)
        estimated_actions = [(action, estimate(action, mins_left - 1, opened)) for action in actions]
        best_score = -1
        for action, max_estimate in sorted(estimated_actions, key=lambda x: x[1], reverse=True):
            if best_score < max_estimate + curr_score:
                # c[(action, mins_left - 1, curr_score, frozenset(opened), node)] += 1
                score = rec_solve(action, mins_left - 1, curr_score, frozenset(opened), node)
                if score > best_score:
                    best_score = score
        if best_score > -1:
            return best_score
        return curr_score

    start = list(graph.keys())[0]
    # c[(start, 30, 0, frozenset(), None)] += 1
    return rec_solve(start, 30, 0, frozenset(), None)


def main():
    graph = load(Path('data/day16.txt'))
    dijkstra_graph = to_dijkstra_graph(graph)
    distances = all_distances(dijkstra_graph)
    print(solve(graph, distances))
    # print(c.most_common(20))


if __name__ == '__main__':
    main()

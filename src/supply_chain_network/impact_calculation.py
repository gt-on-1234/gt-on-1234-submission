import math

import networkx as nx

from .models import ImpactPathAndScore, SupplierIndex, SupplyChainNetwork

# from typing import Generator
# from itertools import pairwise


def to_graph(network: SupplyChainNetwork) -> nx.DiGraph:
    """
    Convert the supply chain network to a directed graph.
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(network)

    for supplier in network.values():
        source = supplier["index"]

        for neighbour in supplier["neighbours"]:
            target = neighbour["index"]
            impact = neighbour["impact"]

            # If the edge already exists, choosing to keep the maximum impact value for that edge
            # as there is not a clear way to combine multiple impacts.
            edge_data = graph.get_edge_data(source, target)

            if edge_data:
                existing_impact = edge_data["impact"]
                impact = max(existing_impact, impact)
                graph[source][target]["impact"] = impact
                graph[source][target]["weight"] = -math.log(impact)
            else:
                if impact > 0:
                    graph.add_edge(
                        source, target, impact=impact, weight=-math.log(impact)
                    )

    return graph


def get_highest_impact_paths_multi_source_dijkstra(
    graph: nx.DiGraph,
    sources: set[str],
    tracked_targets: set[str],
) -> dict[SupplierIndex, ImpactPathAndScore]:
    """
    Compute the highest impact path from any source to each target
    using multi-source Dijkstra.
    """

    distances, paths = nx.multi_source_dijkstra(
        graph,
        sources,
        weight="weight",
    )

    results: dict[str, dict] = {}

    for target in tracked_targets:
        distance = distances.get(target)
        if distance is None:
            continue

        results[target] = {
            "path": paths[target],
            "impact": math.exp(-distance),
        }

    return results


def get_affected_suppliers_multi_source_dijkstra(
    graph: nx.DiGraph,
    sources: set[str],
    tracked_targets: set[str],
    min_impact: float,
) -> set[SupplierIndex]:
    """
    Return targets whose maximum impact from any source
    is greater than or equal to min_impact using multi-source Dijkstra.
    """

    distances = nx.multi_source_dijkstra_path_length(
        graph,
        sources,
        weight="weight",
    )

    affected = set()

    for target in tracked_targets:
        distance = distances.get(target)

        if distance is None:
            continue

        impact = math.exp(-distance)

        if impact >= min_impact:
            affected.add(target)

    return affected


# def _iter_paths(graph: nx.DiGraph, source: str, target: str) -> Generator[tuple[list[str], float]]:
#     """
#     Iterate over all paths from source to target in the graph, yielding the path and its total impact.
#     """

#     for path in nx.all_simple_paths(graph, source=source, target=target):
#         impact = 1.0

#         # for i, j in zip(path, path[1:]):
#         for i, j in pairwise(path):
#             impact *= graph[i][j]["impact"]

#         yield path, impact


# def get_affected_suppliers(graph: nx.DiGraph, sources: set[str], tracked_targets: set[str], min_impact: float) -> set[str]:
#     """
#     Get all suppliers affected by the target supplier.
#     """
#     affected_suppliers = set()

#     for source in sources:
#         for target in tracked_targets:
#             for _, impact in _iter_paths(graph, source=source, target=target):
#                 if impact >= min_impact:
#                     affected_suppliers.add(target)

#     return affected_suppliers


# def get_highest_impact_paths(graph: nx.DiGraph, sources: set[str], tracked_targets: set[str]) -> dict[str, dict]:
#     """
#     Get the highest impact path from any of the sources to each of the tracked targets.
#     """
#     highest_impact_paths = {}

#     for source in sources:
#         for target in tracked_targets:
#             for path, impact in _iter_paths(graph, source=source, target=target):
#                 if target not in highest_impact_paths or impact > highest_impact_paths[target]["impact"]:
#                     highest_impact_paths[target] = {"path": path, "impact": impact}

#     return highest_impact_paths


# def get_highest_impact_paths_dijkstra(
#     graph: nx.DiGraph,
#     sources: set[str],
#     tracked_targets: set[str],
# ) -> dict[str, dict]:
#     """
#     Get the highest impact path from any of the sources to each of the targets using Dijkstra's algorithm.
#     This is more efficient than iterating over all paths, especially for larger graphs.
#     """

#     results = {}

#     for source in sources:

#         distances, paths = nx.single_source_dijkstra(
#             graph,
#             source,
#             weight="weight"
#         )

#         for target in tracked_targets:

#             if target not in distances:
#                 continue

#             impact = math.exp(-distances[target])
#             path = paths[target]

#             if target not in results or impact > results[target]["impact"]:
#                 results[target] = {
#                     "path": path,
#                     "impact": impact
#                 }

#     return results


# def get_affected_suppliers_dijkstra(
#     graph: nx.DiGraph,
#     sources: set[str],
#     tracked_targets: set[str],
#     min_impact: float
# ) -> set[str]:
#     """
#     Get all suppliers affected by the target supplier using Dijkstra's algorithm.
#     This is more efficient than iterating over all paths, especially for larger graphs.
#     """

#     affected_suppliers = set()

#     for source in sources:

#         distances = nx.single_source_dijkstra_path_length(
#             graph,
#             source,
#             weight="weight"
#         )

#         for target in tracked_targets:

#             if target not in distances:
#                 continue

#             impact = math.exp(-distances[target])

#             if impact >= min_impact:
#                 affected_suppliers.add(target)

#     return affected_suppliers

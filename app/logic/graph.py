from abc import ABC, abstractmethod
from typing import Iterable, Tuple, Mapping
from .models import Node
from networkx import nx
import json


class Way:
    def __init__(self, way: Iterable[Node]):
        self.__way = list(way)

    def length(self) -> float:
        s = 0
        for first, second in zip(self.__way[:-1], self.__way[1:]):
            s += first.distance_to(second)
        return s

    def __add__(self, other):
        return Way(self.__way + other.__way)

    def __iter__(self):
        return iter(self.__way)


class Graph(ABC):

    @abstractmethod
    def nodes(self) -> Iterable[Node]:
        pass

    @abstractmethod
    def shortest_way(self, a: int, b: int) -> Way:
        pass

    @abstractmethod
    def __in__(self, node_id: int) -> bool:
        pass

    @abstractmethod
    def add_edge(self, edge: [Node, Node]):
        pass

    def add_edges(self, edges: Iterable[Tuple[Node, Node]]):
        for edge in edges:
            self.add_edge(edge)

    @abstractmethod
    def get_node(self, node_id: int) -> Node:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    def __len__(self) -> int:
        return self.size()


class NxGraph(Graph):
    __graph: nx.Graph = None
    __nodes: Mapping[int, Node] = {}

    def __init__(self, graph_filename: str = None, nodes_filename: str = None):
        if graph_filename:
            self.__graph = nx.read_edgelist(graph_filename, nodetype=int)
        else:
            self.__graph = nx.Graph()

        if nodes_filename:
            with open(nodes_filename, "r") as f:
                nodes = json.load(f)
                self.__nodes = {
                        int(key): Node.from_dict(node)
                        for key, node in nodes.items()
                        }

        self.__sync()

    def __sync(self):
        for node_id in list(self.__nodes):
            if node_id not in self.__graph:
                self.__nodes.pop(node_id)

        for node_id in list(self.__graph.nodes()):
            if node_id not in self.__nodes:
                self.__graph.remove_node(node_id)

    def nodes(self):
        return self.__nodes.values()

    def add_edge(self, edge: [Node, Node]):
        first, last = edge
        self.__nodes[first.id] = first
        self.__nodes[last.id] = last
        self.__graph.add_node(first.id)
        self.__graph.add_node(last.id)
        weight = first.distance_to(last)
        self.__graph.add_edge(first.id, last.id, weight=weight)

    def get_node(self, node_id: int) -> Node:
        return self.__nodes[node_id]

    def size(self) -> int:
        return self.__graph.size()

    def __in__(self, node_id: int) -> bool:
        return node_id in self.__nodes

    def shortest_way(self, a: int, b: int) -> Way:
        way = nx.algorithms.shortest_paths.shortest_path(self.__graph, a, b)
        way = [self.__nodes[node_id] for node_id in way]
        return Way(way)

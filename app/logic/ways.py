from .graph import Graph, Way
from .models import Node
from sklearn.neighbors import NearestNeighbors
import numpy as np
from .geom import elipse_generator


class Pathfinder:

    def __init__(self, graph: Graph, neighbors: int = 1):
        self.__graph = graph
        self.__nbrs = NearestNeighbors(n_neighbors=neighbors)
        self.__fit_neighbors()

    def __fit_neighbors(self):
        data = self.__graph.nodes()
        self.__ids = [node.id for node in data]
        vals = [[node.lon, node.lat] for node in data]
        self.__nbrs.fit(np.array(vals))

    def find_path_betwen_two(
                self,
                first_node: Node,
                last_node: Node,
                r: float,
                accuracy: int = 10
            ) -> Way:
        """
        Finds path betwen first_node and last_node with len at least r.
        Accuracy - number of iterations in search algorithm.
        """

        way = []
        m = 100000  # Minimum distance
        degrees_r = Node.convert_to_degree_distance(r)

        first_neighbors = self.__nbrs.kneighbors(
                [
                    [first_node.lon, first_node.lat],
                ],
                return_distance=False
            )[0]

        last_neighbors = self.__nbrs.kneighbors(
                [
                    [last_node.lon, last_node.lat]
                ],
                return_distance=False
            )[0]


        for start_id in first_neighbors:
            for end_id in last_neighbors:
                start = self.__graph.get_node(self.__ids[start_id])
                end = self.__graph.get_node(self.__ids[end_id])
                for middle_vec in elipse_generator(start.vector, end.vector, degrees_r * 0.75, accuracy):
                    middle_neighbors = self.__nbrs.kneighbors(
                            [(middle_vec.x, middle_vec.y)],
                            return_distance=False
                        )[0]
                    for middle_id in middle_neighbors:
                        current_way = (
                                self.__graph.shortest_way(self.__ids[start_id], self.__ids[middle_id]) +
                                self.__graph.shortest_way(self.__ids[middle_id], self.__ids[end_id])
                            )
                        current_len = current_way.length()

                        if abs(current_len - r) < m:
                            m = abs(current_len - r)
                            way = current_way
        return None if not way else way

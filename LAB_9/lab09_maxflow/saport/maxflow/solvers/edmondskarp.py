from collections import defaultdict

from .solver import AbstractSolver
from ..model import Network

import networkx as nx
from typing import List, Tuple
import time 

class EdmondsKarp(AbstractSolver):

    def solve(self) -> int:
        # basic body for the edmonds-karp algorithm
        max_flow = 0
        rgraph = self.create_residual_graph()
        apath = self.find_augmenting_path(rgraph, self.network.source_node, self.network.sink_node)
        while apath != None:
            max_flow += self.update_residual_graph(rgraph, apath)
            apath = self.find_augmenting_path(rgraph, self.network.source_node, self.network.sink_node)
        return max_flow
        
    def create_residual_graph(self) -> nx.DiGraph:
        rgraph = nx.DiGraph()
        #TODO: 
        # 1) copy all the edges (including capacity attribute) from the original network
        # 2) add edges with 0-capacity in the opposite direction to the original ones
        # rgraph = self.network.digraph.copy()

        for edge in self.network.digraph.edges:
            edge = list(edge)
            capacity = self.network.capacity(self.network.digraph, edge[0], edge[1])

            rgraph.add_edge(edge[0], edge[1])
            self.network.set_capacity(rgraph, edge[0], edge[1], capacity)

            rgraph.add_edge(edge[1], edge[0])
            self.network.set_capacity(rgraph, edge[1], edge[0], 0)

        return rgraph

    def find_augmenting_path(self, graph: nx.DiGraph, src: int, sink: int) -> List[Tuple[int, int]]:
        #TODO:
        # 1) use BFS to find the shortest path between src and sink in the residual graph
        # tip: remember that graphs may have cycles, BFS must not visit the same node twice

        queue = [src]
        paths = {src: []}

        if src == sink:
            return [(src, sink)]

        while queue:
            start_node = queue.pop(0)

            for edge in graph.out_edges(start_node):
                edge = list(edge)
                capacity = self.network.capacity(graph, edge[0], edge[1])
                end_node = edge[1]
                if(capacity > 0) and end_node not in paths:
                    paths[end_node] = paths[start_node] + [(start_node, end_node)]
                    if end_node == sink:
                        return paths[end_node]
                    queue.append(end_node)
        return None

    def update_residual_graph(self, graph: nx.DiGraph, path: List[Tuple[int, int]]) -> int:
        flow = float('inf')
        #TODO: 
        # 1) find flow = min capacity of all the edges on the path
        # 2) for every edge in the path decrease capacity by the flow
        # 3) for every edge opposite to the one in the path, increase its capacity by the flow
        # the flow is then returned to the main body, to join the max flow :)
        caps = []
        for edge in path:
            edge = list(edge)
            caps.append(self.network.capacity(graph, edge[0], edge[1]))

        flow = min(caps)

        for edge in path:
            edge = list(edge)
            actual_capacity = self.network.capacity(graph, edge[0], edge[1])
            self.network.set_capacity(graph, edge[0], edge[1], actual_capacity - flow)

            actual_capacity2 = self.network.capacity(graph, edge[1], edge[0])
            self.network.set_capacity(graph, edge[1], edge[0], actual_capacity2 + flow)

        return flow



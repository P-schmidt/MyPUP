import networkx as nx 
import itertools
import matplotlib as plt
from collections import defaultdict

class Graph():
    def __init__(self, data):
        self.graph = nx.DiGraph()
        self.data = data

        self.create_nodes()
        self.create_edges()
        self.create_home_node()
        self.create_goal_node()

    def get_graph(self):
        """Returns the graph structure."""
        return self.graph
    
    def get_loadtime(self, address):
        return self.graph.nodes[address]['loadtime']

    def create_nodes(self):
        for company in self.data.keys():
            self.graph.add_node(company, loadtime = self.data[company]['loadtime'], 
                                    visited = False, home = False, goal = False) 
        
    
    def create_edges(self):
        for node1, node2 in itertools.combinations(self.graph, 2):
            dist = self.data[node1][node2]
            self.graph.add_edge(node1, node2, duration = dist)
            dist = self.data[node2][node1]
            self.graph.add_edge(node2, node1, duration = dist)

    def create_home_node(self):
        self.graph.nodes['Mypup_home']['home'] = True
        ebunch = []
        for node in self.graph.neighbors('Mypup_home'):
            ebunch.append((node, 'Mypup_home'))
        self.graph.remove_edges_from(ebunch)
        

    def create_goal_node(self):
        self.graph.nodes['Mypup_goal']['goal'] = True
        ebunch = []
        for node in self.graph.neighbors('Mypup_goal'):
            ebunch.append(('Mypup_goal', node))
        self.graph.remove_edges_from(ebunch)
        self.graph.add_edge('Mypup_goal', 'Mypup_home', duration = 0)

    def visualize(self):
        nx.draw(self.graph)
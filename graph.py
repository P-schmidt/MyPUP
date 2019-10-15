import networkx as nx 
import itertools
from collections import defaultdict

class Graph():
    def __init__(self, data):
        self.graph = nx.DiGraph()
        self.data = data
        #TODO adres invullen
        self.mypup = 'Mypup'
        self.create_nodes()
        self.create_edges()
        self.create_home()
        self.create_goal()

    def get_graph(self):
        """Returns the graph structure."""
        return self.graph
    
    def get_loadtime(self, address):
        return self.graph.nodes[address]['loadtime']

    def create_nodes(self):
        for address in self.data.keys():
            self.graph.add_node(address, loadtime = self.data[address]['loadtime'], 
                                         visited = False, home = False) 
        self.graph.nodes[self.mypup]['home'] = True
    
    def create_edges(self):
        for node1, node2 in itertools.combinations(self.graph, 2):
            dist = self.data[node1][node2]
            self.graph.add_edge(node1, node2, duration = dist)
            dist = self.data[node2][node1]
            self.graph.add_edge(node2, node1, duration = dist)

    def create_home(self):
        

    def create_goal(self):


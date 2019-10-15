
class Graph():

    def __init__(self, data):
        # initializes the nodes and edges
        self.data = data
        self.start = "Mypup"
        self.goal = "Mypup"
        self.nodes = {}
        
        print('tester')
        # Dictionary where key is address and value is node
        # object
        self.node_address = {}

        # Create all the nodes in the grid
        self.make_node()
        print("node done")

        # Create all the edges
        # self.create_edges()
    
    def make_node(self):
        # loop through list of nodes and add them
        # if self.goal != None:
        #     self.add_node(self.goal)
        # else:
        for address in self.data.keys():
            Node(address, self.data[address]['loadtime'])   

class Node():
    """
    Node object. This a location in our grid, also includes the
    loadtime attribute which specifies the approximate loading time
    of the address.
    """
    
    def __init__(self, address, loadtime, attr = None):
        self.address = address
        self.loadtime = loadtime
        self.attr = attr
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def delete_edge(self, edge):
        for e in self.edges:
            if e == edge:
                self.edges.remove(e)

    def get_edges(self):
        for edge in self.edges:
            yield edge

    def get_address(self):
        return self.address

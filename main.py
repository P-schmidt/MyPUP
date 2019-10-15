"""Central file from which functions are called. """
import networkx as nx
import pandas as pd
import database as db
from graph import Graph



def main():
    # get a list of addresses and time parameter
    addresses = get_addresses('Addresses.csv')
    print(addresses)
    database = db.init_database(addresses)
    # create graph object with data
    G = Graph(database)
    # HOWTO: retrieve node attr
    # print(G.get_graph().nodes['Amstelvlietstraat 330 Amsterdam'])
    print(G.get_graph().in_edges())
    
    
    # for n in nx.neighbors(G.get_graph(), 'Utrecht'):
        # print(n)

    
    # print(G.get_graph().all_neighbors['Utrecht'])
    
 
def get_addresses(filename):
    """ returns a list of addresses and corresponding time params from address database"""
    df = pd.read_csv(filename)
    return df.values.tolist()
   
main()
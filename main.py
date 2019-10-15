"""Central file from which functions are called. """
import networkx as nx
import pandas as pd
import database as db
from graph import Graph
import unicodedata
import pickle
import random



def main():
    # get a list of addresses and time parameter
    addresses = get_addresses('Mypup_ams_cleaned.csv')
    
    
    #database = db.init_database(addresses)


    # this saves the generated database to a pickle object
    #with open('duration_db.pkl', 'wb') as f:
    #    pickle.dump(database, f)

    # this accesses the saved pickle object
    with open('duration_db.pkl', 'rb') as f:
        database = pickle.load(f)

    #create graph object with data
    G = Graph(database)
    # HOWTO: retrieve node attr
    print('Mypup node:', G.get_graph().nodes['Mypup'])
    

    print('Dist mypup abn GML', G.get_graph().edges['Mypup', 'ABN AMRO GML'])
    
    # for n in nx.neighbors(G.get_graph(), 'Utrecht'):
        # print(n)

    
    # print(G.get_graph().all_neighbors['Utrecht'])
    
 
def get_addresses(filename):
    """ returns a list of addresses and corresponding time params from address database"""
    df = pd.read_csv(filename)
    df['Address'].replace(u'\xa0',u' ', regex=True, inplace=True)
    df['Company'].replace(u'\xa0',u'', regex=True, inplace=True)
    df['Loadtimes'] = random.sample(range(1,100), len(df['Address']))
    return df[['Company', 'Address', 'Loadtimes']].values.tolist()
   
main()
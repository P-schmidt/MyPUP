"""Central file from which functions are called. """

import pandas as pd
import database as db
from graph import Graph



def main():
    # get a list of addresses and time parameter
    addresses = get_addresses('Addresses.xlsx')
    database = db.init_database(addresses)
    graph = Graph(database)


def get_addresses(filename):
    """ returns a list of addresses and corresponding time params from address database"""
    df = pd.read_excel(filename)
    return df.values.tolist()
   
        
    
main()
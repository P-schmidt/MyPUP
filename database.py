# This is the program that initializes the database
# importing required libraries 
import requests 
import json
import pandas as pd
import pickle

def get_addresses(filename):
    """ returns a list of addresses and corresponding time params from address database
        params:
            filename: filename of csv file containing company names and adresses."""
    df = pd.read_csv(filename)
    df['Address'].replace(u'\xa0',u' ', regex=True, inplace=True)
    df['Company'].replace(u'\xa0',u'', regex=True, inplace=True)
    return df[['Company', 'Address']].values.tolist()

# returns the distance and duration between source and destination using Google Maps Distance Matrix API
# Gets the duration or distance between start and end, optional driving mode or cycling
def get_distance(start_address, end_address, duration=True, driving=True):  
    # enter your api key here 
    api_key ='AIzaSyBH_UAuRrdPpzN3BoqlM0OriY7mZkbT_j8'

    # specify units
    units = 'imperial'
    
    # Take source as input 
    source = start_address
    
    # Take destination as input 
    dest = end_address 

    # bydefault driving mode considered
    if driving == True:
        mode = 'driving'
    else:
        mode = 'bicycling'
    # url variable store url  
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?'

    # Get method of requests module 
    # return response object 
    r = requests.get(url+'units='+units+'&mode='+mode+'&origins='+source+'&destinations='+dest+'&key='+api_key)
                        
    # json method of response object 
    # return json format result 
    x = r.json() 

    # return the distance between source and destination
    if duration == True:
        return(x["rows"][0]["elements"][0]["duration"]["value"])
    else:
        return(x["rows"][0]["elements"][0]["distance"]["value"])

def initial_database(filename):
    """Creates a permanent nested dictionary with travel times or distances for each pair of locations in customer base.
        params:
            filename:  file containing company names and addresses for all companies in customer base. """
    addresses = get_addresses(filename)
    database = {}
    for source in addresses:
        database[source[0]] = {}
        for destination in addresses:
            database[source[0]][destination[0]] = get_distance(source[1], destination[1])
    with open('duration_db.pkl', 'wb') as f:
        pickle.dump(database, f)

def add_to_database(new_locs, filename):
    """Adds a new location to the database.
        params:
            location: a list of tuples consisting of the company name and address.
            existing_locs: """
    # open database
    existing_locs = get_addresses(filename)
    
    with open('duration_db.pkl', 'rb') as f:
        database = pickle.load(f)

    # add new locations to database
    for new_loc in new_locs:
        for existing_loc in existing_locs:
            database[new_loc[0]][existing_loc[0]] = get_distance(new_loc[1], existing_loc[1])
            database[existing_loc[0]][new_loc[0]] = get_distance(existing_loc[1], new_loc[1])
    
    # save updated database
    with open('duration_db.pkl', 'wb') as f:
        pickle.dump(database, f)

# make a nested dict with the distances in meters or duration in seconds  between two points, then add loadtime to source


def daily_database(addresses):
    """Creates a list of lists with travel times or distances for each pair of locations. 
        Only considers locations that should be visited on a particular day.
       params: 
            addresses:  dataframe containing company names and addresses,
                        for the locations to be visited on a particular day.  """
    
    with open('duration_db.pkl', 'rb') as f:
        database = pickle.load(f)
    
    daily_database = []
    for source in addresses:
        source_distances = []
        for destination in addresses:
            # find distance in database if possible
            try:
                source_distances.append(database[source][destination])
            except:
                # add location
        daily_database.append(source_distances)
    return database

initial_database('Addresses.csv')
# with open('duration_db.pkl', 'rb') as f:
#     database = pickle.load(f)
# print(database['Paul']['Tidi'])

def create_daily_database(filename):
    # get a list of addresses to visit on particular day
    addresses = get_addresses(filename)
    database = db.init_database(addresses)

    # if create == True:
    #     # this saves the generated database to a pickle object
    data = {}  
    data['distance_matrix'] = database
    data['num_vehicles'] = 5
    data['depot'] = 0
    # print(data)
    # print(data['distance_matrix'])


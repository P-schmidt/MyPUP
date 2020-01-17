# This is the program that initializes the database
# importing required libraries 
import requests 
import json
import pandas as pd
import pickle

def get_info(filename):
    """ returns a list of addresses and corresponding time params from address database
        params:
            filename: filename of csv file containing company names and adresses."""
    df = pd.read_csv(filename+'.csv')
    df['Address'].replace(u'\xa0',u' ', regex=True, inplace=True)
    df['Company'].replace(u'\xa0',u'', regex=True, inplace=True)
    return df[['Company', 'Address', 'Loadtimes', 'Timewindow']].values.tolist()

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
            filename:  filename indicates what customer base should be retrieved from database. """
    
    addresses = get_info(filename)
    print(addresses)
    database = {}


    for source in addresses:
        print(source)
        # add metadata for location
        database[source[0]] = {}
        database[source[0]]['Address'] = source[1]
        database[source[0]]['Loadtime'] = source[2]
        database[source[0]]['Timewindow'] = source[3]


        # calculate distances to all other locations 
        for destination in addresses:
            database[source[0]][destination[0]] = get_distance(source[1], destination[1])
        print(source[0], 'is done')
    with open(filename+'.pkl', 'wb') as f:
        pickle.dump(database, f)

def add_to_database(new_loc, filename):
    """Adds new locations to the database.
        params:
            new_loc: a list consisting of the company name, address and load time. <- is het niet slimmer om dit uit de CSV te halen dan het met de hand in te moeten voeren
            filename:  filename indicates what customer base should be retrieved from database. """
    
    # open database  
    with open(filename+'.pkl', 'rb') as f:
        database = pickle.load(f)

    # add metadata for location
    database[new_loc[0]] = {}
    database[new_loc[0]]['Address'] = new_loc[1]
    database[new_loc[0]]['Loadtime'] = new_loc[2] 

    # calculate distances to each existing location 
    for existing_loc in database.keys():
        database[new_loc[0]][existing_loc] = get_distance(new_loc[1], database[existing_loc]['Address'])
        database[existing_loc][new_loc[0]] = get_distance(database[existing_loc]['Address'], new_loc[1])

    # save updated database
    with open(filename+'.pkl', 'wb') as f:
        pickle.dump(database, f)

def update_database(column, filename):
    """Adds new locations to the database.
        params:
            new_locs: a list of lists consisting of the company name, address and load time.
            filename:  filename indicates what customer base should be retrieved from database. """

    updated_data = get_info(filename)

    if column == 'Company':
        index = 0
    elif column == 'Address':
        index = 1
    elif column == 'Loadtime':
        index = 2
    elif column == 'Timewindow':
        index = 3
    else:
        print('update_database terminated because column:', column, 'does not exist')
        exit()
    
    # open database  
    with open(filename+'.pkl', 'rb') as f:
        database = pickle.load(f)

    # loop through all locations and update the relevant
    for location in updated_data:
        database[location[0]][column] = location[index]

    # save updated database
    with open(filename+'.pkl', 'wb') as f:
        pickle.dump(database, f)


def remove_from_database(rem_loc, filename):
    """Removes locations from the database
        params: 
            rem_loc: names of companies to remove.
            filename:  filename indicates what customer base should be retrieved from database. """
    
    # open database  
    with open(filename+'.pkl', 'rb') as f:
        database = pickle.load(f)

    # remove all instances of location in database
    del database[rem_loc]
    for loc in database.keys():
        del database[loc][rem_loc]
    
    # save updated database
    with open(filename+'.pkl', 'wb') as f:
        pickle.dump(database, f)

def database_list(filename):
    with open(filename+'.pkl', 'rb') as f:
        database = pickle.load(f)
    locations_list = [loc for loc in database.keys()]
    return locations_list

def distance(filename, source, dest):
    with open(filename+'.pkl', 'rb') as f:
        database = pickle.load(f)
    print(database[source][dest])

def create_distance_matrix(filename, companies):
    """ Returns distance matrix.
        Only considers locations that should be visited on a particular day.
       params: 
            companies:  list containing company names for the locations to be visited on a particular day.  
            filename:  name of file with company info (without extension)"""

    with open(filename+'.pkl', 'rb') as f:
        database = pickle.load(f)

    #print(database['Booking.com Atrium'])

    distance_matrix = []
    for source in companies:
        source_distances = []
        for destination in companies:
            # find distance in database if possible
            try:
                source_distances.append(database[source][destination])
            except:
                print(f"ERROR:{source} of {destination} niet in database/pickle.")
                exit(0)  
        distance_matrix.append(source_distances)
    return distance_matrix


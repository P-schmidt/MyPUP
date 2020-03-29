# This is the program that initializes the database
# importing required libraries 
import requests 
import json
import pandas as pd
import pickle
from ast import literal_eval

def get_info(filename):
    """ returns a list of addresses and corresponding time params from address database
        params:
            filename: filename of csv file containing company names and adresses."""
    df = pd.read_csv(filename+'.csv')
    df['Address'].replace(u'\xa0',u' ', regex=True, inplace=True)
    df['Company'].replace(u'\xa0',u'', regex=True, inplace=True)
    return df[['Company', 'Address', 'Loadtimes', 'Demands', 'Timewindow']].values.tolist()

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

    database = {}

    for source in addresses:
        # add metadata for location
        database[source[0]] = {}
        database[source[0]]['Address'] = source[1]
        database[source[0]]['Loadtime'] = source[2]
        database[source[0]]['Demands'] = source[3]
        database[source[0]]['Timewindow'] = source[4]


        # calculate distances to all other locations 
        for destination in addresses:
            database[source[0]][destination[0]] = get_distance(source[1], destination[1])
        print(source[0], 'is done')
    with open(filename+'.pkl', 'wb') as f:
        pickle.dump(database, f)

def add_to_database(new_loc, filename):
    """Adds new locations to the database.
        params:
            new_loc: a list consisting of the company name, address, load time, demand and time window. <- is het niet slimmer om dit uit de CSV te halen dan het met de hand in te moeten voeren
            filename:  filename indicates what customer base should be retrieved from database. """
    
    # open database  
    with open(filename+'.pkl', 'rb') as f:
        database = pickle.load(f)

    # add metadata for location
    database[new_loc[0]] = {}
    database[new_loc[0]]['Address'] = new_loc[1]
    database[new_loc[0]]['Loadtime'] = new_loc[2] 
    database[new_loc[0]]['Demands'] = new_loc[3]
    database[new_loc[0]]['Timewindow'] = new_loc[4]  

    # calculate distances to each existing location 
    for existing_loc in database.keys():
        database[new_loc[0]][existing_loc] = get_distance(new_loc[1], database[existing_loc]['Address'])
        database[existing_loc][new_loc[0]] = get_distance(database[existing_loc]['Address'], new_loc[1])

    # save updated database
    with open(filename+'.pkl', 'wb') as f:
        pickle.dump(database, f)

def update_database(column, filename):
    """Updates a column in the database according to the specified file.
        params:
            column: The column that should be retrieved and updated in the pickle.
            filename:  filename indicates what customer base should be retrieved from database. """

    updated_data = get_info(filename)

    if column == 'Company':
        index = 0
    elif column == 'Address':
        index = 1
    elif column == 'Loadtime':
        index = 2
    elif column == 'Demands':
        index = 3
    elif column == 'Timewindow':
        index = 4
    else:
        print('update_database terminated because column:', column, 'does not exist')
        exit()

    # open database
    with open(filename+'.pkl', 'rb') as f:
        database = pickle.load(f)

    print(updated_data)


    # loop through all locations and update the relevant column
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

def create_database(filename, company_list, capacities=[200, 200, 200, 200, 200], create=False):

    # call this function if you want to create a new pickle with distances
    if create == True:
        initial_database(filename)

    # this function can be used to add a company to the database pickle
    #add_to_database(['Infinity', 'Amstelveenseweg 500, 1081 KL Amsterdam NL', 5], 'Mypup_bakfiets')

    # this function can be used to update a column in the pkl
    # update_database('Demands', filename)

    with open(filename+'.pkl', 'rb') as f:
        database_pickle = pickle.load(f)

    daily_company_loadtimes = []
    # get all the load times of the companies and append them in order to list
    for company in company_list:
        daily_company_loadtimes.append(database_pickle[company]['Loadtime'])

    daily_company_timewindows = []
    # get the time windows for the companies and append them in order to list
    for company in company_list:
        daily_company_timewindows.append(literal_eval(database_pickle[company]['Timewindow']))

    daily_company_demands = []
    # get the demands for the companies and append them in order to list
    for company in company_list:
        daily_company_demands.append(database_pickle[company]['Demands'])

    # initialize the data as a dict and add keys with their values
    data = {}
    data['distance_matrix'] = create_distance_matrix(filename, company_list)
    data['loadtimes'] = daily_company_loadtimes
    data['demands'] = daily_company_demands
    data['vehicle_capacities'] = capacities
    data['num_vehicles'] = len(data['vehicle_capacities'])
    data['depot'] = 0
    data['time_windows'] = daily_company_timewindows
    data['initial_routes'] = [
         [0, 2, 18, 33, 26, 1, 49, 34, 5, 6, 0],
         [0, 14, 36, 38, 39, 37, 8, 30, 10, 12, 9, 0],
         [0, 13, 43, 42, 44, 11, 0],
         [0, 17, 50, 29, 27, 47, 35, 3, 24, 7, 15, 0],
         [0, 31, 28, 16, 4, 46, 41, 0]
              ]
              
    return data






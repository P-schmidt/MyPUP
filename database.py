# This is the program that initializes the database
# importing required libraries 
import requests 
import json



# returns the distance and duration between source and destination using Google Maps Distance Matrix API
# Gets the duration or distance between start and end, optional driving mode or cycling
def get_distance(start_address, end_address, duration, driving):  
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

# make a nested dict with the distances in meters or duration in seconds  between two points, then add loadtime to source
def init_database(addresses, duration=True, driving=True):
    database = {}
    i = 0
    for source in addresses:
        database[source[0]] = {}
        for destination in addresses:
            if source[0] == destination[0]:
                continue
            database[source[0]][destination[0]] = get_distance(source[1], destination[1], duration, driving)
            i += 1
            if i%100 == 0:
                print(i)
        database[source[0]]['loadtime'] = source[2]
    return database



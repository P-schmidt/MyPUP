# This is the program that initializes the database
# importing required libraries 
import requests 
import json

# get a list of addresses and time parameter
addresses = [["Amstelvlietstraat 330 Amsterdam", 10], ["Kinkerstraat 10 Amsterdam", 20], ["Centraal station Amsterdam", 30], ["Utrecht", 100]]

# returns the distance and duration between source and destination using Google Maps Distance Matrix API
def get_distance(start_address, end_address):  
    # enter your api key here 
    api_key ='AIzaSyBH_UAuRrdPpzN3BoqlM0OriY7mZkbT_j8'

    # specify units
    units = 'imperial'
    
    # Take source as input 
    source = start_address
    
    # Take destination as input 
    dest = end_address 
    
    # url variable store url  
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?'

    # Get method of requests module 
    # return response object 
    r = requests.get(url+'units='+units+'&origins='+source+'&destinations='+dest+'&key='+api_key)
                        
    # json method of response object 
    # return json format result 
    x = r.json() 
    # bydefault driving mode considered 
    
    # return the distance between source and destination
    return(x["rows"][0]["elements"][0]["distance"]["value"])

# make a nested dict with the distances in meters between two points, then add loadtime to source
def init_database(addresses):
    for source in addresses:
        database[source[0]] = {}
        for destination in addresses:
            if source == destination:
            continue
            database[source[0]][destination[0]] = get_distance(source[0], destination[0])
        database[source[0]]['loadtime'] = source[1]


database = {}
init_database(addresses)
print('database:',database)


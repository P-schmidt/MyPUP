# https://www.google.com/maps/dir/Prinsengracht+219A,+1015+DT+Amsterdam/Amstelvlietstraat+330,+Amsterdam,+Netherlands/Kolenkitbuurt,+Amsterdam/@52.3618908,4.8383503,13z voorbeeld link
import webbrowser
import time
import pickle

def create_url(list_of_addresses):

    clean_addresses = []
    for address in list_of_addresses:
        address = address.replace(' NL', '')
        address = address.replace('t/m ', '')
        address = address.replace(',', '')
        address = address.replace(' ', '+')
        clean_addresses.append(address)

    url = "https://www.google.com/maps/dir/"
    extra_url = "https://www.google.com/maps/dir/"

    # loop through addresses
    for i, address in enumerate(clean_addresses):
        if i < 10:
            url += address+'/'
        else:
            extra_url += address+'/'
    
    if extra_url != "https://www.google.com/maps/dir/":
        webbrowser.get('firefox').open_new(url)
        time.sleep(2)
        webbrowser.get('firefox').open_new_tab(extra_url)
    else:
        webbrowser.get('firefox').open_new(url)

def open_maps(filename, list_of_routes):
    with open(filename+'.pkl', 'rb') as f:
        database_pickle = pickle.load(f)

    list_of_addresses = []
    for route in list_of_routes:
        if route != ['Mypup', 'Mypup']:
            addresses_of_route = []
            for i, company in enumerate(route):
                source = database_pickle[company]['Address']
                #destination = database_pickle[route[i+1]]['Address']
                addresses_of_route.append(source)
            list_of_addresses.append(addresses_of_route)

    # creates a list of urls for every route, url is a link to google maps with the route
    list_of_urls = []
    for route in list_of_addresses:
        list_of_urls.append(create_url(route))

    return list_of_urls
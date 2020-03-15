"""Vehicles Routing Problem (VRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ast import literal_eval
import database as db
import visualizer as vs
import pandas as pd
import random
import pickle


def create_database(filename, company_list, capacities=[200, 200, 200, 200, 200], create=False):

    # call this function if you want to create a new pickle with distances
    if create == True:
        db.initial_database(filename)

    # this function can be used to add a company to the database pickle
    #db.add_to_database(['Infinity', 'Amstelveenseweg 500, 1081 KL Amsterdam NL', 5], 'Mypup_bakfiets')

    # this function can be used to update a column in the pkl
    # db.update_database('Demands', filename)

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
    data['distance_matrix'] = db.create_distance_matrix(filename, company_list)
    data['loadtimes'] = daily_company_loadtimes
    data['demands'] = daily_company_demands
    print('Total demands = ', sum(data['demands']))
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

def print_solution(data, manager, routing, assignment, company_list):
    """Prints assignment on console."""
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    total_demand = 0
    total_loading_time = 0
    total_waiting_time = 0
    list_of_routes =[]
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_demand = 0
        loading_time = 0
        wait_time = 0
        companies_on_route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            time_var = time_dimension.CumulVar(index)
            route_demand += data['demands'][node_index]
            loading_time += data['loadtimes'][node_index]
            wait_time += assignment.Max(time_var) - assignment.Min(time_var)
            plan_output += '{0} Time({1},{2}) -> '.format(
                company_list[node_index], round(assignment.Min(time_var)/60),
                round(assignment.Max(time_var)/60))
            companies_on_route.append(company_list[node_index])
            index = assignment.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(company_list[manager.IndexToNode(index)],
                                                    round(assignment.Min(time_var)/60),
                                                    round(assignment.Max(time_var)/60))
        companies_on_route.append(company_list[manager.IndexToNode(index)])
        plan_output += 'Time of the route: {}min\n'.format(
            round(assignment.Min(time_var)/60))
        plan_output += 'Demand of the route: {}\n'.format(route_demand)
        plan_output += 'Loading times of the route: {} minutes\n'.format(loading_time)
        plan_output += 'Waiting time of the route: {} minutes'.format(round(wait_time/60))
        list_of_routes.append(companies_on_route)
        print(plan_output)
        print('Total travelling time of route: {} min\n'.format(round(assignment.Min(time_var)/60-loading_time)))
        total_demand += route_demand
        total_loading_time += loading_time
        total_time += assignment.Min(time_var)
        total_waiting_time += wait_time
    print('Total travelling of all routes: {} min'.format(round(total_time/60-total_loading_time)))
    print('Total loading time of all routes: {} min'.format(round(total_loading_time)))
    print('Total demand of all routes: {}'.format(total_demand))
    print('Waiting time of the route: {} minutes'.format(round(total_waiting_time/60)))

    return list_of_routes

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
        list_of_urls.append(vs.create_url(route))

    return list_of_urls

def main(companies_to_remove=[], visualise=False):
    """Solve the CVRP problem."""
    filename = 'data/Mypup_bus'

    # create a list with all the companies as daily_company_list tester
    df = pd.read_csv(filename+'.csv')
    df['Company'].replace(u'\xa0',u'', regex=True, inplace=True)
    company_list = df['Company'].values.tolist()

    # this is the list of companies that have no packages to be delivered
    companies_to_remove = ['HUT Beursstraat', 'HUT Warmoesstraat', 'HVA DMH', 'HVA FMB',
                            'HVA NTH', 'Nieuw Amsterdam', 'Spicalaan Hoofddorp',
                            'UVA SP904', 'Ymere']

    # removes the companies to be skipped from the company_list
    [company_list.remove(company) for company in companies_to_remove]

    print('Total number of companies to be visited', len(company_list))

    # Instantiate the data problem.
    data = create_database(filename, company_list)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        # data['demands'] adds the loading time to the travel time
        return (data['loadtimes'][from_node] * 60) + data['distance_matrix'][from_node][to_node]

    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        # print('index = ', from_index)
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
        

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        2000,  # allow waiting time
        28400,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(data['time_windows'][0][0],
                                                data['time_windows'][0][1])
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC)

    print('start solving')
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # # Print solution on console. (with own solution printer)
    # if assignment:
    #     total_optimized_distance, list_of_routes = print_solution(data, manager, routing, assignment, company_list)

    if assignment:
        print('aangekomen')
        list_of_routes = print_solution(data, manager, routing, assignment, company_list)

    #print(f'The overall travelling time that is saved is {round((total_initial_distance-total_optimized_distance)/60)} minutes')

    #this prints the routes as a list of lists with adresses
    if visualise == True:
        open_maps(filename, list_of_routes)



if __name__ == '__main__':
    main()
"""Vehicles Routing Problem (VRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import database2 as db
import pandas as pd
import random
import pickle


def create_database(filename, company_list, create=True):
    
    # if create == True:
    #     # get a list of addresses and time parameter
    #     addresses = get_addresses(filename)
    #     database = db.init_database(addresses)

    #     data = {}
    #     data['distance_matrix'] = database
    #     data['num_vehicles'] = 5
    #     data['depot'] = 0
    #     # this saves the generated database to a pickle object
    #     with open('duration_db.pkl', 'wb') as f:
    #         pickle.dump(data, f)
    # else:
    #     with open('duration_db.pkl', 'rb') as f:
    #         data = pickle.load(f)

    
    # get the loadtimes of the daily_company_list


    db.daily_database(company_list, filename)

    with open(filename+'.pkl', 'rb') as f:
        database_pickle = pickle.load(f)

    daily_company_loadtimes = []
    # get all the load times of the companies and append them in order to list
    for company in company_list:
        daily_company_loadtimes.append(database_pickle[company]['Loadtime'])
    
    print('loadingtimes:', daily_company_loadtimes)

    # initialize the data as a dict and add keys with their values
    data = {}
    data['distance_matrix'] = db.daily_database(company_list, filename)
    data['num_vehicles'] = 7
    data['demands'] = daily_company_loadtimes
    print(sum(data['demands']))
    data['vehicle_capacities'] = [120, 120, 120, 120, 120, 80, 80]
    print(sum(data['vehicle_capacities']))
    data['depot'] = 0
    # data['initial_routes'] = [
    #     [8, 16, 14, 13, 12, 11],
    #     [3, 4, 9, 10],
    #     [15, 1],
    #     [7, 5, 2, 6],
    # ]
    return data

def print_solution(data, manager, routing, assignment, company_list):
    """Prints assignment on console."""
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(company_list[node_index], route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(company_list[manager.IndexToNode(index)],
                                                 route_load)
        plan_output += 'Travelling time of the route: {}minutes\n'.format(round(route_distance/60))
        plan_output += 'Loading time of the route: {} minutes\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total travelling time of all routes: {}minutes'.format(round(total_distance/60)))
    print('Total loading time of all routes: {}'.format(total_load))

def main():
    """Solve the CVRP problem."""
    filename = 'Mypup_ams_cleaned'

    # create a list with all the companies as daily_company_list tester
    df = pd.read_csv(filename+'.csv')
    df['Company'].replace(u'\xa0',u'', regex=True, inplace=True)
    company_list = df['Company'].values.tolist()

    # this is the list of companies that we need to visit on this route
    #company_list = ['Mypup', 'Joan Muyskenweg 4', 'Joan Muyskenweg 6', 'HVA KSH', 'HVA WBH', 'UVA BH / OIH', 'UVA HVA LWB Privé' , 'UVA PCH', 'UVA REC ABC', 'UVA REC M', 'UVA UB Singel 425']

    # Instantiate the data problem.
    data = create_database(filename, company_list)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
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

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        print_solution(data, manager, routing, assignment, company_list)


if __name__ == '__main__':
    main()
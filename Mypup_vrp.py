"""Vehicles Routing Problem (VRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import database2 as db
import pandas as pd
import random
import pickle


def create_database(filename, company_list, create=True):
    # get the loadtimes of the daily_company_list
    db.create_distance_matrix(filename, company_list)

    with open(filename+'.pkl', 'rb') as f:
        database_pickle = pickle.load(f)

    daily_company_loadtimes = []
    # get all the load times of the companies and append them in order to list
    for company in company_list:
        daily_company_loadtimes.append(database_pickle[company]['Loadtime'])

    # initialize the data as a dict and add keys with their values
    data = {}
    data['distance_matrix'] = db.create_distance_matrix(filename, company_list)
    data['num_vehicles'] = 9
    data['demands'] = daily_company_loadtimes
    print(sum(data['demands']))
    data['vehicle_capacities'] = [180, 180, 180, 180, 180, 80, 80, 80, 80]
    print(sum(data['vehicle_capacities']))
    data['depot'] = 0
    data['initial_routes'] = [
         [0, 22, 59, 78, 45, 43, 75, 53, 3, 34, 7, 17, 0],
         [0, 48, 5, 6, 77, 52, 30, 32, 1, 40, 49, 50, 51, 0],
         [0, 35, 36, 37, 38, 71, 60, 21, 62, 44, 18, 61, 73, 74, 2, 0],
         [0, 29, 16, 55, 56, 57, 54, 9, 47, 11, 13, 10, 0],
         [0, 15, 14, 27, 28, 20, 64, 63, 65, 12, 76, 0],
         [0, 42, 41, 58, 46, 67, 33, 31, 69, 70, 66, 68, 72, 0],
         [0, 4, 8, 19, 39, 23, 24, 25, 26, 0],
         [],
         [],

     ]
    return data

# prints the solution that was calculated by algorithm
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
    return total_distance

# prints the initial solution
def print_initial_solution(data, company_list):
    initial_routes = 'initial_routes'
    total_distance = 0
    total_loadtime = 0
    for vehicle_id in range(data['num_vehicles']):
        if data[initial_routes][vehicle_id] != []:
            whole_route = f"Route for vehicle {vehicle_id} start at {company_list[data[initial_routes][vehicle_id][0]]} -> "
            distance = 0
            loadtime = 0
            for i in range(0, len(data['initial_routes'][vehicle_id])-1):
                source = data[initial_routes][vehicle_id][i]
                destination = data[initial_routes][vehicle_id][i+1]
                whole_route += f'{company_list[data[initial_routes][vehicle_id][i]]} -> '
                distance += data['distance_matrix'][source][destination]
                loadtime += data['demands'][source]
            whole_route += f'-> {company_list[data[initial_routes][vehicle_id][0]]}'
            distance += data['distance_matrix'][data[initial_routes][vehicle_id][len(data['initial_routes'][vehicle_id])-1]][len(data['initial_routes'][vehicle_id])]
            print(whole_route)
            print(f'total time driven is {round(distance/60)}')
            print(f'total loadtime is {loadtime}\n')
            total_distance += distance
        else:
            print(f'Vehicle {vehicle_id} is not used in this solution\n')
    print(f'The total time driven is {round(total_distance/60)}\n')
    return total_distance

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

    total_initial_distance = print_initial_solution(data, company_list)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        total_optimized_distance = print_solution(data, manager, routing, assignment, company_list)

    print(f'The overall travelling time that is saved is {round((total_initial_distance-total_optimized_distance)/60)} minutes')

if __name__ == '__main__':
    main()
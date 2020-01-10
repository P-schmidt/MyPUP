"""Vehicles Routing Problem (VRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import database2 as db
import pandas as pd
import random
import pickle


def create_data_model(filename, company_list):
    # get the loadtimes of the daily_company_list
    db.create_distance_matrix(filename, company_list)

    with open(filename+'.pkl', 'rb') as f:
        database_pickle = pickle.load(f)
    
    daily_company_loadtimes = []
    # get all the load times of the companies and append them in order to list
    for company in company_list:
        daily_company_loadtimes.append(database_pickle[company]['Loadtime'])

    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = db.create_distance_matrix(filename, company_list)
    data['num_vehicles'] = 7
    data['depot'] = 0

    return data


def print_solution(data, manager, routing, solution, company_list):
    """Prints solution on console."""
    max_route_distance = 0
    list_of_routes = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        companies_on_route = []
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(company_list[manager.IndexToNode(index)])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Traveltime of the route: {}m\n'.format(round(route_distance/60))
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum travel time of route: {}m'.format(round(max_route_distance/60)))




def main():
    filename = 'Mypup_ams_cleaned'

    # create a list with all the companies as daily_company_list tester
    df = pd.read_csv('Mypup_bus'+'.csv')
    df['Company'].replace(u'\xa0',u'', regex=True, inplace=True)
    company_list = df['Company'].values.tolist()

    print(company_list)

    # this is the list of companies that have no packages to be delivered
    #companies_to_remove = ['HVA FMB','HVA DMH', 'HVA NTH', 'Nieuw Amsterdam', 'Quarter Avenue', 'Quarter Podium']

    # removes the companies to be skipped from the company_list
    #[company_list.remove(company) for company in companies_to_remove]
    
    print('Total number of companies to be visited', len(company_list))

    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model(filename, company_list)

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

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        5000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution, company_list)


if __name__ == '__main__':
    main()
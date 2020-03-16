from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import visualizer as vs
import database as db
import printer as pt
import pandas as pd
import pickle
import copy
from random import randint

def vrp_script(data, company_list, printer=False):
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
        500,  # allow waiting time
        10000,  # maximum time per vehicle
        True,  # Don't force start cumul to zero.
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
        routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)
        #GEBRUIK NU PATH_MOST_CONSTRAINED_ARC

    # sets the time limit in seconds
    search_parameters.time_limit.seconds = 5

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    if assignment:
        if printer == True:
            list_of_routes, time = pt.print_solution(data, manager, routing, assignment, company_list)
        else:
            list_of_routes, time = pt.create_list_of_routes(data, manager, routing, assignment, company_list)
        return list_of_routes, time

    return 0, 0


def main(companies_to_remove=[], visualise = False, init_compare = True, sample=False):
    """main function sets route planning function in motion. Takes the following arguments:
        companies_to_remove(optional) : list of companies that should not be taken into account for route planning.
        visualise(optional) : Google Maps pages with routes are created if True.
        init_compare(optional) : comparison with initial routes is made if True.
        sample(optional) : a random sample of companies is removed from planning if True."""

    capacities = [200, 200, 200, 200, 200]

    filename = 'data/Mypup_bus'

    # create a list with all the companies as daily_company_list tester
    df = pd.read_csv(filename+'.csv')
    df['Company'].replace(u'\xa0',u'', regex=True, inplace=True)
    company_list = df['Company'].values.tolist()

    # make a shallow copy of company list to be used for initial routes
    initial_company_list = copy.copy(company_list)

    # this is the list of companies that have no packages to be delivered
    # companies_to_remove = ['Spicalaan Hoofddorp', 'HUT Beursstraat', 'HUT Warmoesstraat', 'HVA DMH', 'HVA FMB', 'HVA NTH']

    # creates a list of index numbers for the companies that are removed.
    index_numbers = []
    for i in range(len(initial_company_list)):
        if initial_company_list[i] in companies_to_remove:
            index_numbers.append(i)
    
    
    #create random numbers, and remove the companies belonging to those spots.
    if sample:
        for _ in range(4):
            number = randint(0, len(company_list)) - 1
            if number != 0:
                index_numbers.append(number)
                companies_to_remove.append(company_list[number])
                # companies_to_remove.append(initial_company_list[number])
            else:
                pass
    
    print("Verwijderde bedrijven:")
    for comp in set(companies_to_remove):
        print(comp)
    print("\n")

    # removes the companies to be skipped from the company_list
    [company_list.remove(company) for company in set(companies_to_remove)]
    
    print(f"Totaal aantal te bezoeken bedrijven: {len(company_list)} \n")
    # Instantiate the data problem.
    data = db.create_database(filename, company_list, capacities)

    # if necessary create data for init routes
    if init_compare == True:
        data2 = db.create_database(filename, initial_company_list, capacities)
        new_init_routes = []
        for route in data2['initial_routes']:
            new_route = [location for location in route if location not in set(index_numbers)]
            new_init_routes.append(new_route)
        
        
        data2['initial_routes'] = new_init_routes

        total_initial_time = pt.print_initial_solution(data2, initial_company_list)

    data['vehicle_capacities'] = capacities
    data['num_vehicles'] = len(capacities)

    loadfactor = 1
    vehicles_used = 6

    routes, total_optimized_time = vrp_script(data, company_list, printer=False)
    if routes:
        routes = [route for route in routes if route != ['Mypup', 'Mypup']]
        vehicles_used = len(routes)
    
    while vehicles_used > 5 or routes is 0:
        data['vehicle_capacities'].append(200)
        data['num_vehicles'] = len(data['vehicle_capacities'])
        routes, total_optimized_time = vrp_script(data, company_list, printer=False)

        if routes is 0 or data['num_vehicles'] == 8:
            # print(data['num_vehicles'])
            data['vehicle_capacities'] = [200, 200, 200, 200, 200]
            data['num_vehicles'] = len(data['vehicle_capacities'])
            loadfactor = round(loadfactor - 0.1, 2)
            data['loadtimes'] = [loadtime * loadfactor for loadtime in data['loadtimes']]
            # print(f'loadfactor: {loadfactor}')
        else:
            # print(data['num_vehicles'])
            # print(f'else loadfactor: {loadfactor}')
            routes = [route for route in routes if route != ['Mypup', 'Mypup']]
            vehicles_used = len(routes)

    # used to print the routes with correct parameters
    routes, total_optimized_time = vrp_script(data, company_list, printer=True)

    print(f"Resulting capacities: {data['vehicle_capacities']} and loadfactor: {loadfactor}")

    # get rid of routes that contain no mypup->mypup routes
    routes = [route for route in routes if route != ['Mypup', 'Mypup']]

    print(f"The optimized driving time is {round(total_optimized_time)}")

    if init_compare == True:
        print(f"The difference between init and optimized = {total_initial_time-total_optimized_time}")

    print(f"Number of vehicles used in optimized solution: {len(routes)}\n")

    # visualises the routes if set to true
    if visualise == True:
        vs.open_maps(filename, routes)



if __name__ == '__main__':
    main()
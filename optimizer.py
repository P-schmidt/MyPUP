from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ast import literal_eval
import bus_vrp_tw as vrp
import database as database
import pandas as pd
import pickle
import copy


def create_list_of_routes(data, manager, routing, assignment, company_list):
    """Prints assignment on console."""
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    total_load = 0
    list_of_routes =[]
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route_load = 0
        companies_on_route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            time_var = time_dimension.CumulVar(index)
            route_load += data['demands'][node_index]
            companies_on_route.append(company_list[node_index])
            index = assignment.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        companies_on_route.append(company_list[manager.IndexToNode(index)])
        list_of_routes.append(companies_on_route)
        total_load += route_load
        total_time += assignment.Min(time_var)
    total_time = round(total_time/60)
    print(f"total load = {total_load}")
    print(f"total time = {total_time}")
    print(f"total travel time = {total_time-total_load}")

    return list_of_routes, total_time-total_load

def vrp_script(data, company_list):
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
        return (data['demands'][from_node]*60) + data['distance_matrix'][from_node][to_node]

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
        2000,  # allow waiting time
        14400,  # maximum time per vehicle
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

    # sets the capacity constraint
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
        routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC)

    # sets the time limit in seconds
    search_parameters.time_limit.seconds = 5

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    if assignment:
        #things = vrp.print_solution(data, manager, routing, assignment, company_list)
        list_of_routes, time = create_list_of_routes(data, manager, routing, assignment, company_list)
        return list_of_routes, time

    return 0, 0

# prints the initial solution
def print_initial_solution(data, company_list):
    initial_routes = 'initial_routes'
    total_distance = 0
    total_loadtime = 0
    for vehicle_id in range(data['num_vehicles']):
        if data[initial_routes][vehicle_id] != []:
            whole_route = f"Route for vehicle {vehicle_id} start at "
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


def main(visualise = False, init_compare = True):
    correct = 0
    capacities = [150, 200, 200, 200, 200]

    filename = 'data/Mypup_bus'

    # create a list with all the companies as daily_company_list tester
    df = pd.read_csv(filename+'.csv')
    df['Company'].replace(u'\xa0',u'', regex=True, inplace=True)
    company_list = df['Company'].values.tolist()

    # make a shallow copy of company list to be used for initial routes
    initial_company_list = copy.copy(company_list)

    # this is the list of companies that have no packages to be delivered
    companies_to_remove = ['HUT Beursstraat', 'HUT Warmoesstraat', 'HVA DMH', 'HVA FMB',
                            'HVA NTH', 'Ijland', 'Nieuw Amsterdam', 'Spicalaan Hoofddorp',
                            'UVA SP904', 'Ymere']

    # removes the companies to be skipped from the company_list
    [company_list.remove(company) for company in companies_to_remove]

    print(f'companies to be driven = {len(company_list)}\n')

    # Instantiate the data problem.
    data = vrp.create_database(filename, company_list, capacities)

    # if necessary create data for init routes
    if init_compare == True:
        data2 = vrp.create_database(filename, initial_company_list, capacities)
        initial_names = []
        for route in data2['initial_routes']:
            names = [initial_company_list[index] for index in route]
            initial_names.append(names)
        #if wanted visualise the orgiginal routes
        if visualise == True:
            vrp.open_maps(filename, initial_names)


    while True:
        routes, total_optimized_time = vrp_script(data, company_list)
        if routes == 0:
            capacities.append(50)
            # print(f"new capcities = {capacities} \n")
            data = vrp.create_database(filename, company_list, capacities)
        else:
            break

    print(f"optimized time = {total_optimized_time}\n")

    if init_compare == True:
        print(f"difference = {total_initial_distance-total_optimized_time}\n")

    for route in routes:
        if route != ['Mypup', 'Mypup']:
            print(route, "\n")

    used_routes = [route for route in routes if route != ['Mypup', 'Mypup']]

    # print("Amount of vehicles used: ", len(used_routes))

    if visualise == True:
        vrp.open_maps(filename, used_routes)



if __name__ == '__main__':
    main()
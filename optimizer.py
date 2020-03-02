from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ast import literal_eval
import bus_vrp_tw as vrp
import database as database
import pandas as pd
import pickle
import multiprocessing
import time

#handler for alarm signal
def handler(signum, frame):
   print("Forever is over!")
   raise Exception("end of time")

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
            companies_on_route.append(company_list[node_index])
            index = assignment.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        companies_on_route.append(company_list[manager.IndexToNode(index)])
        list_of_routes.append(companies_on_route)
        total_load += route_load
        total_time += assignment.Min(time_var)

    return list_of_routes

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


    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    if assignment:
        list_of_routes = create_list_of_routes(data, manager, routing, assignment, company_list)
        return list_of_routes

    return 0



def main():
    correct = 0
    capacities = [150, 200, 200, 200, 200, 50, 50, 50]

    filename = 'data/Mypup_bus'

    # create a list with all the companies as daily_company_list tester
    df = pd.read_csv(filename+'.csv')
    df['Company'].replace(u'\xa0',u'', regex=True, inplace=True)
    company_list = df['Company'].values.tolist()

    # this is the list of companies that have no packages to be delivered
    companies_to_remove = ['Newday Offices Almere']

    # removes the companies to be skipped from the company_list
    [company_list.remove(company) for company in companies_to_remove]

    # Instantiate the data problem.
    data = vrp.create_database(filename, company_list, capacities)

    # signal.signal(signal.SIGALRM, handler)

    used_routes = []

    routes = vrp_script(data, company_list)

    used_routes = [route for route in routes if route != ['Mypup', 'Mypup']]

    print(len(used_routes))

    # while(correct == 0):
    #     if sum(capacities) < sum(data['demands']):
    #         capacities.append(capacities[-1])
    #         print(capacities)
    #     signal.alarm(10)
    #     try:
    #         routes = vrp_script(data)
    #         print(routes)
    #         if routes != []:
    #             print('aangekomen')
    #             break
    #     except Exception, exc:
    #         print('exception')
    #         capacities.append(capacities[-1])
    #     signal.alarm(0)


    #run vrp solver in while loop
    #change vrp_solver to only return list of routes
    #everytime check if solution is correct
    #if correct run again with visualizer



if __name__ == '__main__':
    main()
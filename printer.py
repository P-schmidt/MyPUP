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
        plan_output += 'Loading times of the route: {} minutes\n'.format(round(loading_time))
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

    return list_of_routes, round(total_time/60-total_loading_time)

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
            route_load += data['loadtimes'][node_index]
            companies_on_route.append(company_list[node_index])
            index = assignment.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        companies_on_route.append(company_list[manager.IndexToNode(index)])
        list_of_routes.append(companies_on_route)
        total_load += route_load
        total_time += assignment.Min(time_var)
    total_time = round(total_time/60)

    return list_of_routes, round(total_time-total_load)

def print_initial_solution(data, company_list):
    initial_routes = 'initial_routes'
    total_distance = 0
    # total_loadtime = 0
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
            # print(whole_route)
            # print(f'total time driven is {round(distance/60)}')
            # print(f'total loadtime is {loadtime}\n')
            total_distance += distance
        else:
            print(f'Vehicle {vehicle_id} is not used in this solution')
    print(f'The initial total drive time is {round(total_distance/60)}')
    return round(total_distance/60)
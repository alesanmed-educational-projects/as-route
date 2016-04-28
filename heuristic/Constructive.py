# -*- coding: utf-8 -*-
import numpy as np
import heuristic.utils as utils

from heuristic.Graph import TSP_Graph
from heuristic.Solution import Solution

def random_solution(graph, customers_list):
    if not isinstance(graph, TSP_Graph):
        utils.raise_value_error(graph, TSP_Graph, type(graph))
    
    if not isinstance(customers_list, list):
        utils.raise_value_error(customers_list, list, type(customers_list))
        
    customers = np.empty((len(customers_list),), 
                         dtype=[('id', 'i4'), ('ws', 'i8'), ('t', 'i8')])
    
    for i, customer in enumerate(customers_list):
        depot_pos = graph.get_customer_index(0)        
        c_pos = graph.get_customer_index(customer.get_id())
        customers[i] = (customer.get_id(), 
                                 customer.get_window_start(), 
                                 graph.get_time(depot_pos, c_pos))
    
    # Almacen siempre el primero, su ventana empieza en 0 y el tiempo hasta si
    # mismo es 0    
    customers = customers[np.argsort(customers, order=('ws', 't'))]
    
    solution = Solution(len(customers_list))
    
    solution.set_graph(graph)
    solution.set_solution(customers['id'])
    
    
    start_time = int(customers['ws'][1] - customers['t'][1])
    if start_time < 0:
        start_time = 0

    solution.set_start_time(start_time)
    
    curr_time = start_time
    for i, c_id in enumerate(solution.get_solution()):
        customer = next((c for c in customers_list if c.get_id() == c_id), None)
        time_visited = curr_time + customers['t'][i]

        if time_visited < customer.get_window_start():
            time_visited = customer.get_window_start()
        
        customer.set_time_visited(int(time_visited))
        curr_time = time_visited
    
    solution.set_customer_list(customers_list)
    
    return solution
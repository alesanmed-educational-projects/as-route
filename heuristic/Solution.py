# -*- coding: utf-8 -*-
import numpy as np
import heuristic.utils as utils

from heuristic.Graph import TSP_Graph
from heuristic.Customer import Customer

class Solution:
    
    def __init__(self, n_customers, solution=None):
        if solution is not None and isinstance(solution, self):
            self.solution = solution.get_solution()
            self.start_time = solution.get_start_time()
            self.graph = solution.get_graph()
            self.distances = solution.get_distances()
            self.customers_list = solution.get_customers_list()
            self.valid_customers = solution.get_valid_customers()
            self.time_cost = solution.get_time_cost()
            self.distance_cost = solution.get_distance_cost()
            self.solution_cost = solution.get_solution_cost()
        else:
            # Orden de visita de los clientes
            self.solution = np.empty((n_customers, 1))
            self.start_time = 0
            self.graph = None
            self.distances = None
            self.customers_list = None
            self.valid_customers = None
            self.time_cost = None
            self.distance_cost = None
            self.solution_cost = None

    def get_start_time(self):
        return self.get_start_time

    def set_start_time(self, start_time):
        if not isinstance(start_time, int):
           utils.raise_value_error("start_time", int, type(start_time))

        self.start_time = start_time
    
    def get_graph(self):
        return self.graph
        
    def set_graph(self, graph):
        if not isinstance(graph, TSP_Graph):
            utils.raise_value_error("graph", TSP_Graph, type(graph))
            
        self.graph = graph
    
    def get_distances(self):
        return self.distances
        
    def set_distances(self, distances):
        if not isinstance(distances, TSP_Graph):
            utils.raise_value_error("distances", TSP_Graph, type(distances))
            
        self.distances = distances
    
    def get_customers_list(self):
        return self.customers_list
    
    def set_customer_list(self, customers_list):
        if not isinstance(customers_list, list):
            utils.raise_value_error("customers_list", list, type(customers_list))
        
        self.customers_list = customers_list
    
    def get_solution(self):
        return self.solution
        
    def set_solution(self, solution):
        if not isinstance(solution, np.ndarray):
            utils.raise_value_error("solution", np.ndarray, type(solution))
        
        self.solution = solution
    
    def get_valid_customers(self):
        if self.valid_customers is None:
            raise NameError("valid_customers not setted yet")
        
        return self.valid_customers
        
    def is_solution_valid(self):
        if self.valid_customers is None:
            self.compute_validity()
    
        return np.all(self.valid_customers == True)
    
    def compute_validity(self):
        if self.graph is None:
            raise NameError("graph not setted yet")
        
        if self.customers_list is None:
            raise NameError("customer_list not setted yet")
        
        valid_customers = np.empty(len(self.get_customers_list()))
        for i, c_row in enumerate(self.solution):
            to_find = Customer(-1, 0, 0)
            to_find.set_row(c_row)
            
            customer_index = self.get_customers_list().index(to_find)
            
            if customer_index == -1:
                raise KeyError("Solution does not contains all of the customers. \
                                Have you generated a solution yet?")
                                
            valid_customers[i] = self.get_customers_list()[customer_index].is_valid()
        
        self.valid_customers = valid_customers
        
    def get_time_cost(self):
        if self.graph is None:
            raise NameError("graph not setted yet")
        
        if self.customers_list is None:
            raise NameError("customer_list not setted yet")
        
        if self.time_cost is None:
            last_customer = Customer(-1, 0, 0)
            last_customer.set_row(self.get_solution()[-1])
            
            last_customer = self.get_customers_list()[self.get_customers_list().index(last_customer)]

            time = last_customer.get_time_visited()
            
            if time < last_customer.get_window_start():
                time = last_customer.get_window_start()

            time += self.get_graph().get_value(last_customer.get_row(), self.get_solution()[0])
            self.time_cost = time
        
        return self.time_cost
        
    def compute_distances(self):
        if self.get_solution() is None:
            raise NameError("solution not generated yet")
        
        self.solution_cost = np.empty((self.get_solution().size - 1, 1))

        for i in range(len(self.get_solution())):
            if i == len(self.solution) - 1:
                break
            
            origin_index = self.get_solution()[i]
            destination_index = self.get_solution()[i + 1]
            
            self.solution_cost[i] = self.get_distances().get_value(origin_index, destination_index)
            
        
    def get_distance_cost(self):
        if self.solution_cost is None:
            self.compute_distances()
        
        if self.distance_cost is None:
            self.distance_cost = np.sum(self.solution_cost)
            
            last_customer = self.get_solution()[-1]
            depot = self.get_solution()[0]
            
            self.distance_cost += self.get_distances().get_value(last_customer, depot)
        
        return self.distance_cost
        
    def one_shift(self, old_pos, new_pos):
        self.update_costs_shift(old_pos, new_pos)

        if old_pos > new_pos:
            self.distance_cost = None
            self.solution = np.concatenate((self.solution[0:new_pos],
                                            self.solution[old_pos],
                                            self.solution[new_pos:old_pos],
                                            self.solution[old_pos + 1:]))
        elif old_pos < new_pos:
            self.distance_cost = None
            self.solution = np.concatenate((self.solution[0:old_pos],
                                            self.solution[old_pos + 1:new_pos],
                                            self.solution[old_pos],
                                            self.solution[new_pos:]))

    
    def update_costs_shift(self, old_index, new_index):
        if old_index > new_index:
            solution = self.get_solution()
            self.solution_cost = np.concatenate((self.solution_cost[0:new_index - 1],
                                                 [self.get_distances().
                                                 get_value(solution[new_index - 1], 
                                                           solution[old_index]),
                                                 self.get_distances().
                                                 get_value(solution[old_index], 
                                                           solution[new_index + 1])],
                                                 self.solution_cost[new_index:old_index - 1],
                                                 [self.get_distances().
                                                 get_value(solution[old_index - 1],
                                                           solution[old_index + 1])],
                                                 self.solution_cost[old_index + 1:]
                                                ))
        elif old_index < new_index:
            solution = self.get_solution()
            self.solution_cost = np.concatenate((self.solution_cost[0:new_index - 1],
                                                 [self.get_distances().
                                                 get_value(solution[old_index - 1],
                                                           solution[old_index + 1])],
                                                 self.solution_cost[old_index + 1:new_index - 1],
                                                 [self.get_distances().
                                                 get_value(solution[new_index - 1], 
                                                           solution[old_index]),
                                                 self.get_distances().
                                                 get_value(solution[old_index], 
                                                           solution[new_index + 1])],
                                                 self.solution_cost[new_index:]
                                                ))
    
    def recompute_validity(self, index):
        valid_customers = np.empty(self.valid_customers.shape)
        if index == 1:
            depot = Customer(0, 0, 0)
            
            depot = self.get_customers_list()[self.get_customers_list().index(depot)]
            
            first_customer = Customer(-1, 0, 0)
            first_customer.set_row(self.get_solution()[1])
            
            first_customer = self.get_customers_list()[self.get_customers_list().index(first_customer)]
            
            depot_time = first_customer.get_window_start() - self.get_graph().get_value(depot.get_row(), first_customer.get_row())
            
            if depot_time < 0:
                depot_time = 0
                
            depot.set_time_visited(depot_time)
            valid_customers[0] = depot.is_valid()
        else:
            valid_customers[0:index] = self.valid_customers[0:index]
        

        for i, c_row in enumerate(self.solution[index:]):
            to_find = Customer(-1, 0, 0)
            to_find.set_row(c_row)
            
            customer_index = self.get_customers_list().index(to_find)
            
            if customer_index == -1:
                raise KeyError("Solution does not contains all of the customers. \
                                Have you generated a solution yet?")
            
            customer = self.get_customers_list[customer_index]
            
            prev_customer_row = self.get_solution()[index + i - 1]
            prev_customer = Customer(-1, 0, 0)
            prev_customer.set_row(prev_customer_row)
            
            prev_customer = self.get_customers_list()[self.get_customers_list().index(prev_customer)]
            
            time_visited_customer = prev_customer.get_time_visited() + \
                                    self.get_graph().get_value(
                                        prev_customer_row, c_row)
                                        
            if time_visited_customer < customer.get_window_start():
                time_visited_customer = customer.get_window_start()

            customer.set_time_visited(time_visited_customer)
            
            valid_customers[i + index] = customer.is_valid()
            
        self.valid_customers = valid_customers

    def __str__(self):
        sol = []
        for c_row in self.get_solution():
            sol.append(self.get_graph().get_customer_id(c_row))

        return sol.__str__()
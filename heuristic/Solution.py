# -*- coding: utf-8 -*-
import numpy as np
import heuristic.utils as utils

from heuristic.Graph import TSP_Graph

class Solution:
    
    def __init__(self, n_customers):
        # Orden de visita de los clientes
        self.solution = np.empty((n_customers, 1))
        self.start_time = 0
        self.graph = None
        self.customers_list = None
        self.valid_customers = None

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
        for i, c_id in enumerate(self.solution):
            customer = next((c for c in self.get_customers_list() if c.get_id() == c_id), None)
            
            if customer is None:
                raise KeyError("Solution does not contains all of the customers. \
                                Have you generated a solution yet?")
                                
            valid_customers[i] = customer.is_valid()
        
        self.valid_customers = valid_customers
        
    def __str__(self):
        return self.get_solution().__str__()
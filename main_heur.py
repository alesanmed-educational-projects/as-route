# -*- coding: utf-8 -*-
from heuristic.Customer import Customer
from heuristic.Graph import TSP_Graph
from heuristic.Constructive import random_solution
from maps.acme_database import get_customers
from maps.matrices import get_matrices


ids = [0, 1, 2, 3, 4]

customers = get_customers(ids)

customers_ids = customers['id']

customers_coords = [coords.replace(b';', b',').decode('utf-8') for coords in customers['c']]

data = get_matrices(customers_coords)

graph = TSP_Graph(customers_ids.size)
graph.set_ids(customers_ids)
graph.set_time_matrix(data[0])

customers_list = []
for customer in customers:
    customers_list.append(Customer(customer['id'], customer['ws'], customer['we']))
    
solution = random_solution(graph, customers_list)

print(solution)
print(solution.is_solution_valid())
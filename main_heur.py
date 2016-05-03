# -*- coding: utf-8 -*-
from heuristic.Customer import Customer
from heuristic.Graph import TSP_Graph
from heuristic.Constructive import random_solution, perturbation, local1shift
from maps.acme_database import get_customers
from maps.matrices import get_matrices


ids = [0, 1, 2, 3, 4]

customers = get_customers(ids)

customers['ws'][1] = 6*60*60
customers['we'][1] = 12*60*60
customers['ws'][2] = 6*60*60
customers['we'][2] = 12*60*60

customers['ws'][3] = 12*60*60
customers['we'][3] = 18*60*60
customers['ws'][4] = 12*60*60
customers['we'][4] = 18*60*60

customers_ids = customers['id']

customers_coords = [coords.replace(b';', b',').decode('utf-8') for coords in customers['c']]

data = get_matrices(customers_coords)

time_graph = TSP_Graph(customers_ids.size)
time_graph.set_ids(customers_ids)
time_graph.set_matrix(data[0])

distance_graph = TSP_Graph(customers_ids.size)
distance_graph.set_ids(customers_ids)
distance_graph.set_matrix(data[1])

customers_list = []
for customer in customers:
    customer_obj = Customer(customer['id'], customer['ws'], customer['we'])
    customer_obj.set_row(distance_graph.get_customer_index(customer['id']))
    
    customers_list.append(customer_obj)

level = 1    
levelMax = 100
solution = random_solution(time_graph, customers_list)
solution.set_distances(distance_graph)

solution = local1shift(solution)

while not solution.is_solution_valid() and level < levelMax:
    improved_sol = perturbation(solution, level)
    improved_sol = local1shift(improved_sol)
    
    if improved_sol.get_constructive_obj() < solution.get_constructive_obj():
        solution = improved_sol
        level = 1
    else:
        level += 1

print(solution)
print(solution.is_solution_valid())
print(solution.get_time_cost())
print(solution.get_distance_cost())
print(solution.get_valid_customers())
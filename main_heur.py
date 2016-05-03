# -*- coding: utf-8 -*-
import numpy as np
import os

from heuristic.Customer import Customer
from heuristic.Graph import TSP_Graph
from heuristic.Constructive import random_solution, perturbation, local1shift
from heuristic.VND import vnd
from maps.acme_database import get_customers
from maps.matrices import get_matrices


ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

customers = get_customers(ids)

customers['ws'][1] = 6*60*60
customers['we'][1] = 12*60*60
customers['ws'][2] = 6*60*60
customers['we'][2] = 12*60*60
customers['ws'][3] = 6*60*60
customers['we'][3] = 12*60*60
customers['ws'][4] = 6*60*60
customers['we'][4] = 12*60*60

customers['ws'][5] = 12*60*60
customers['we'][5] = 18*60*60
customers['ws'][6] = 12*60*60
customers['we'][6] = 18*60*60
customers['ws'][7] = 12*60*60
customers['we'][7] = 18*60*60
customers['ws'][8] = 12*60*60
customers['we'][8] = 18*60*60
customers['ws'][9] = 12*60*60
customers['we'][9] = 18*60*60


customers_ids = customers['id']

customers_coords = [coords.replace(b';', b',').decode('utf-8') for coords in customers['c']]

if os.path.isfile('matrices.npy'):
    data = np.load('matrices.npy')
else:    
    data = get_matrices(customers_coords)
    np.save('matrices.npy', data)

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

best_sol = None
iterMax = 100
for _ in range(iterMax):
    level = 1    
    levelMax = 100
    solution = random_solution(time_graph, customers_list)
    solution.set_distances(distance_graph)
    
    solution = local1shift(solution)
    
    while not solution.is_valid() and level < levelMax:
        improved_sol = perturbation(solution, level)
        improved_sol = local1shift(improved_sol)
        
        if improved_sol.get_constructive_obj() < solution.get_constructive_obj():
            solution = improved_sol
            level = 1
        else:
            level += 1
            
    print("Finished constructive phase. Found valid solution: {0}".format(solution.is_valid()))
    
    if solution.is_valid():
        print(solution)
        level = 1
        solution = vnd(solution)
        
        while level < levelMax:
            improved_sol = perturbation(solution, level)
            improved_sol = vnd(improved_sol)
            
            if improved_sol.get_distance_cost() < solution.get_distance_cost():
                solution = improved_sol
                level = 1
            else:
                level += 1
    
    if best_sol is None:
        best_sol = solution
    elif not best_sol.is_valid() and solution.is_valid():
        best_sol = solution
    elif solution.get_distance_cost() < best_sol.get_distance_cost():
        best_sol = solution
        
print(best_sol)
print(best_sol.is_valid())
print(best_sol.get_time_cost())
print(best_sol.get_distance_cost())
print(best_sol.get_valid_customers())
# -*- coding: utf-8 -*-
import numpy as np
import os

from heuristic.Customer import Customer
from heuristic.Graph import TSP_Graph
from heuristic.TPH import TPH
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

tph = TPH(20, 30)
tph.set_customers_ids(customers_ids)
tph.set_customers_list(customers_list)
tph.set_distance_matrix(data[1])
tph.set_time_matrix(data[0])

best_sol = tph.run()
        
print(best_sol)
print(best_sol.is_valid())
print(best_sol.get_time_cost())
print(best_sol.get_distance_cost())
print(best_sol.get_valid_customers())
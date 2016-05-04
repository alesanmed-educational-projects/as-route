import numpy as np
import matplotlib.pyplot as plt
import time

from maps.acme_database import get_customers
from exact.Dumas import Dumas
from exact.read_file import from_google_maps
from heuristic.Customer import Customer
from heuristic.Graph import TSP_Graph
from heuristic.TPH import TPH

def time_exact(n, customers):
    data = np.load('maps/matrices{0}.npy'.format(n))
    time_matrix = data[0]
    
    t = time.time()
    graph = from_google_maps(customers, time_matrix)
    dumas = Dumas(graph)
    solution = dumas.run()
    return time.time() - t, solution.is_feasible()

def time_heuristic(n, customers):
    data = np.load('maps/matrices{0}.npy'.format(n))
    customers_ids = customers['id']    
    
    t = time.time()
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

    tph = TPH(20, 50, optimize='t')
    tph.set_customers_ids(customers_ids)
    tph.set_customers_list(customers_list)
    tph.set_distance_matrix(data[1])
    tph.set_time_matrix(data[0])
    
    best_sol = tph.run()
    
    return time.time() - t, best_sol.is_valid()

def run():
    N_values = [9, 11, 13, 14]
    times_exact = []
    feasible_exact = []
    
    times_heur = []
    feasible_heur = []
    for n in N_values:
        if n == 9:
            ids = [0, 3, 7, 14, 18, 5, 11, 15, 19, 1]
        elif n == 11:
            ids = [0, 3, 7, 14, 18, 31, 5, 11, 15, 19, 1, 2]
        elif n == 13:
            ids = [0, 3, 7, 14, 18, 31, 5, 11, 15, 19, 22, 1, 2, 4]
        elif n == 14:
            ids = [0, 3, 7, 14, 18, 31, 33, 5, 11, 15, 19, 22, 23, 2, 4]
            
        customers = get_customers(ids)
        
        exact_time, exact_feasible = time_exact(n, customers)
        heur_time, heur_feasible = time_heuristic(n, customers)        
        
        times_exact.append(exact_time)
        if exact_feasible:
            feasible_exact.append('g')
        else:
            feasible_exact.append('r')       
        
        times_heur.append(heur_time)
        if heur_feasible:
            feasible_heur.append('g')
        else:
            feasible_heur.append('r')
    
    fig = plt.figure()
    plt.plot(N_values, times_exact)
    plt.scatter(N_values, times_exact, c=feasible_exact)
    plt.plot(N_values, times_heur)
    plt.scatter(N_values, times_heur, c=feasible_heur)
    plt.legend(['Dumas', 'TPH'], loc='upper left')
    plt.savefig('test-res.png', dpi=271, bbox_inches='tight')
    fig.clear()
    plt.close('all')

if __name__=="__main__":
    run()

        


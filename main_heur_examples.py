# -*- coding: utf-8 -*-

from heuristic.Customer import Customer
from heuristic.TPH import TPH
from heuristic.read_file import lopez_ibanez_blum_format


data, customers = lopez_ibanez_blum_format('heuristic/examples/n20w20.001.txt')

time_matrix = data[0]
distance_matrix = data[1]
customers_list = customers[0]
customers_ids = customers[1]

tph = TPH(20, 100, optimize='t')
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
for customer in best_sol.get_solution():
    c = Customer(customer, 0, 0)
    print(best_sol.get_customers_list()[best_sol.get_customers_list().index(c)])
    
# -*- coding: utf-8 -*-
import argparse
import os
import numpy as np

from exact.read_file import from_google_maps, lopez_ibanez_blum_format
from exact.Dumas import Dumas
from datetime import date, datetime, timedelta
from pymongo import MongoClient
from maps.acme_database import today_customers, today_purchases
from maps.matrices import get_matrices

def run_acmesupermarket():
	purchases = today_purchases()
	customers = today_customers()
	customers_coords = [coords.replace(b';', b',').decode('utf-8') for coords in customers['c']]

	today = datetime.utcnow().date()
	route = {
		'day' : today.day,
		'month': today.month,
		'year': today.year
	}

	if len(customers):

		if os.path.isfile('matrices.npy'):
			data = np.load('matrices.npy')
		else:    
			data = get_matrices(customers_coords)
			np.save('matrices.npy', data)
		time_matrix = data[0]

		searchingSolution = True
		while (searchingSolution):

			for c in customers:
				print(c)
			
			graph = from_google_maps(customers, time_matrix)
			dumas = Dumas(graph)
			sol = dumas.run()
			print("-----------")
			print(sol)
			print(sol.times)
			print(sol.is_feasible())
			print(sol.total_cost())

			if sol.is_feasible():
				searchingSolution = False
			else:
				deleted_customer = customers[-1]
				customers = np.delete(customers,-1)
				tomorrow = datetime.date.today() + datetime.timedelta(days=1)
				for purchase in purchases:
					if purchase['customer_id']==deleted_customer['id']:
						result = db.purchases.update_one(
							{"_id": purchase['_id']},
							{"$set": {"deliveryDate": tomorrow}}
						)

		result_customers = []
		for vertex in sol.vertices:
			if vertex.label=='start':
				result_customers.append(-1)
			elif vertex.label=='end':
				result_customers.append(-1)
			else:
				result_customers.append(int(vertex.label))

		route['customers'] = result_customers
		route['times'] = sol.times


	else:
		route['customers'] = []
		route['times'] = []

	print(route)

	#client = MongoClient()
	#db = client['Acme-Supermarket']
	#db.routes.insert_one(route)

def run_example():
	n = input("Numero de clientes [10-14]: ")
	graph = lopez_ibanez_blum_format('exact/examples/n20w'+n+'.001.txt')
	dumas = Dumas(graph)
	sol = dumas.run()
	print("-----------")
	print(sol)
	print(sol.times)
	print(sol.is_feasible())
	print(sol.total_cost())

if __name__=="__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-s", "--source", required=True, choices=[
                    'example', 'Acme-Supermarket'],
                    help="Data source used: Example /\
                     Acme-Supermarket DB")
	args = vars(ap.parse_args())
	if args['source']=='example':
		run_example()
	else:
		run_acmesupermarket()
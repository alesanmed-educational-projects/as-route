# -*- coding: utf-8 -*-
import os
import numpy as np

from exact.read_file import from_google_maps
from exact.Dumas import Dumas

from datetime import date, timedelta

from pymongo import MongoClient

from datetime import datetime
from maps.acme_database import today_customers, today_purchases
from maps.matrices import get_matrices

purchases = today_purchases()
customers = today_customers()
for c in customers:
	print(c)
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

	searchingSolution = False
	while (searchingSolution):
		
		graph = from_google_maps(customers, time_matrix)
		dumas = Dumas(graph)
		sol = dumas.run()
		print("-----------")
		print(sol)
		print(sol.times)
		print(sol.vertices)
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
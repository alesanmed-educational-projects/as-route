# -*- coding: utf-8 -*-
import numpy as np

from pymongo import MongoClient

def get_customers(ids):
    customers = np.empty((len(ids),), dtype=[('id', 'i4'), ('c', 'S40'), ('ws', 'i4'), ('we', 'i4')])
    
    connection = MongoClient()
    db = connection['Acme-Supermarket']
    
    for i, id in enumerate(ids):
        if id == 0:
            customer = {
                '_id' : id,
                'coordinates': "37.4019025;-5.986620499999958",
                'window_start': 0,
                'window_end': 24*60*60
            }
        else:
            customer = db.actors.find({'_id': id})[0]
        # El tercero sera la ventana de tiempo. Cada cosa en su momento
        customers[i] = (int(customer['_id']), str(customer['coordinates']), 0, 24*60*60)

    return customers
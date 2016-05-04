# -*- coding: utf-8 -*-
import numpy as np

from datetime import datetime, timedelta
from pymongo import MongoClient

def today_customers():
    purchases = today_purchases()

    customers_ids = [0]
    
    for purchase in purchases:
        if purchase['customer_id'] not in customers_ids:
            customers_ids.append(purchase['customer_id'])

    return get_customers(customers_ids)[:10] # TODO: Solo los diez primeros de momentos

def today_purchases():
    connection = MongoClient()
    db = connection['Acme-Supermarket']

    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(1)
    #db.purchases.find({'deliveryTime': {'$gte': start, '$lt': end}})
    #TODO: de momento cogemos todas las compras, luego cogemos las 10 primeras.

    purchases = []
    for doc in db.purchases.find():
        purchases.append(doc)

    return purchases

def get_customers(ids):
    customers = np.empty((len(ids),), dtype=[('id', 'i4'), ('c', 'S40'), ('ws', 'i4'), ('we', 'i4')])

    connection = MongoClient()
    db = connection['Acme-Supermarket']
    
    for i, id in enumerate(ids):
        if id == 0:
            customer = {
                '_id' : id,
                'coordinates': "37.358380;-5.988009",
                'window_start': 0*60*60,
                'window_end': 24*60*60
            }
        else:
            customer = db.actors.find({'_id': id})[0]
            if customer['timeWindow']=='MORNING':
                customer['window_start'] = 8*60*60
                customer['window_end'] = 14*60*60
            elif customer['timeWindow']=='AFTERNOON':
                customer['window_start'] = 14*60*60
                customer['window_end'] = 20*60*60
            elif customer['timeWindow']=='BOTH':
                customer['window_start'] = 8*60*60
                customer['window_end'] = 20*60*60
            else:
                raise ValueError('TimeWindow of customer' + str(id) + 
                    ' invalid: ' + customer['timeWindow'])

        customers[i] = (int(customer['_id']), str(customer['coordinates']), 
            customer['window_start'], customer['window_end'])

    return customers
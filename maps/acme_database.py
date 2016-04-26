# -*- coding: utf-8 -*-
from pymongo import MongoClient

def get_customers(ids):
    customers = []
    
    connection = MongoClient()
    db = connection['Acme-Supermarket']
    
    for id in ids:
        customer = db.actors.find({'_id': id})[0]
        # El tercero sera la ventana de tiempo. Cada cosa en su momento
        customers.append([customer['_id'], customer['coordinates'], -1])
    
    return customers
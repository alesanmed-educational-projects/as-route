# -*- coding: utf-8 -*-
import numpy as np

class TSP_Graph:
    def __init__(self, n_customers):
        self.time_matrix = np.empty((n_customers, n_customers))
        
    def set_ids(self, customer_ids):
        self.customer_ids = customer_ids
    
    def get_time(self, i, j):
        return self.time_matrix[i, j]
        
    def set_time(self, i, j, time):
        self.time_matrix[i, j] = time
    
    def get_time_matrix(self):
        return self.time_matrix
    
    def set_time_matrix(self, time_matrix):
        if not isinstance(time_matrix, np.ndarray):
            time_matrix = np.array(time_matrix)            
            
        if time_matrix.shape != self.time_matrix.shape:
            raise ValueError("The input matrix shape is not equal to the \
                                graph's matrix shape. Original shape: {0}. \
                                New shape: {1}"
                                .format(self.time_matrix.shape,
                                        time_matrix.shape))
                                        
        self.time_matrix = time_matrix
        
    def get_customer_index(self, customer_id):
        if self.customer_ids is None:
            raise NameError("customer_ids vector not setted yet")
        
        customer_index = np.where(self.customer_ids == customer_id)[0]
        
        if not customer_index.size:
            raise KeyError("Customer Id does not exists")
        
        return customer_index[0]
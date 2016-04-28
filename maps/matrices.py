# -*- coding: utf-8 -*-
import googlemaps
import numpy as np

def get_matrices(coords):
    gmaps = googlemaps.Client(key='AIzaSyDvEP-1BzJIAL-hY2WTu6xZKTBiqrsJHbE')
    
    res = gmaps.distance_matrix(coords, coords)
    
    coords_len = len(coords)
    time_matrix = np.empty((coords_len, coords_len))
    distance_matrix = np.empty((coords_len, coords_len))
    
    for row, dict in enumerate(res['rows']):
        for column, element in enumerate(dict['elements']):
            time_matrix[row, column] = element['duration']['value']
            distance_matrix[row, column] = element['distance']['value']
    
    return [time_matrix, distance_matrix]
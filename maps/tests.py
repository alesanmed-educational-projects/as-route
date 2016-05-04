# -*- coding: utf-8 -*-
import numpy as np

from matrices import get_matrices
from acme_database import get_customers

ids = [0, 3, 7, 14, 18, 31, 33, 5, 11, 15, 19, 22, 23, 2, 4]

customers = get_customers(ids)

customers_coords = [coords.replace(b';', b',').decode('utf-8') for coords in customers['c']]

data = get_matrices(customers_coords)
np.save('matrices{0}.npy'.format(len(ids) - 1), data)
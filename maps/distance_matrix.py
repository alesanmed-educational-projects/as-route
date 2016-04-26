# -*- coding: utf-8 -*-

import googlemaps

gmaps = googlemaps.Client(key='AIzaSyDvEP-1BzJIAL-hY2WTu6xZKTBiqrsJHbE')

origins = ["San Francisco, CA, USA", "Victoria, BC, Canada"]
destinations = ["Vancouver, BC, Canada", "Seattle, WA, USA"]

res = gmaps.distance_matrix(origins, destinations)

print(res['rows'])
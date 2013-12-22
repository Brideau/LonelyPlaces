# This scans the entire country for various
# types of places and retrieves the nearest
# one to a grid of points.

from createcitieslist import cities_list
from threading import Lock
from createthreads import create_threads
from outputnearest import output_nearest_place

# Used to prevent file write issues later
print_lock = Lock()

# Fredericton
lat_NW = 45.998931
lng_NW = -66.748867
lat_SE = 45.870202
lng_SE = -66.550709

# Grid size
increment = 0.0035961575091  # 400 m

# Select which places of interest you'd like to
# scan.

# places = ['grocery_or_supermarket', 'art_gallery', 'library']
# places = ['art_gallery', 'library']
places = ['grocery_or_supermarket', 'hospital', 'art_gallery', 'library']

# Print CSV header
print('place, lat, lng, latnear, lngnear, dist_km')

# I got my centroid list from here: http://geocoder.ca/?freedata=1
cities = cities_list("library/geodata/canada_cities.csv")

# Has the grid split up into threads and processed
for place in places:
    create_threads(output_nearest_place, cities, place, print_lock,
                   increment=increment, numthreads=10)

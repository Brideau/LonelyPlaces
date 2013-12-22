# This scans the entire country for various
# types of places and retrieves the nearest
# one to a grid of points.

from threadcallcapi import create_threads
from createcitieslist import cities_list

# Select which places of interest you'd like to
# scan. Note that for areas with a large land
# mass like Canada, you may go over Google's
# 100,000 daily API call limit if you scan too
# many at once.

# places = ['grocery_or_supermarket', 'art_gallery', 'library']
# places = ['art_gallery', 'library']
places = ['grocery_or_supermarket', 'hospital', 'art_gallery', 'library']

# Print CSV header
print('place, lat, lng, latnear, lngnear, dist_miles')

# I got my centroid list from here: http://geocoder.ca/?freedata=1
cities = cities_list("library/geodata/canada_cities.csv")

# Has the grid split up into threads and processed
for place in places:
    create_threads(10, cities, place)

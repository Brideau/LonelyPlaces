# This scans the entire country for various
# types of places and retrieves the nearest
# one to a grid of points.

from random import randrange
import time
import requests
from math import sqrt, ceil
from threading import Lock, Thread
from googleapikey import GOOGLE_API_KEY
from distancesphere import distance_on_unit_sphere
from generatesearchlocations import create_area_grid, cities_list

# Prevents write issues from threading
print_lock = Lock()

scan_type = "grid"  # grid/citylist
scale = "small"  # small/large: the size of the area being scanned
if scan_type == "list":
    list_name = "library/geodata/canada_cities.csv"

# Places to scan
places = ['grocery_or_supermarket', 'library']
# places = ['grocery_or_supermarket', 'art_gallery', 'library']
# places = ['art_gallery', 'library']
# places = ['grocery_or_supermarket', 'hospital', 'art_gallery']

if scale == "small":
    increment = 0.0035961575091  # 400m
else:
    increment = 0.2697118131790  # 30km

# Print CSV header
print('place, lat, lng, latnear, lngnear, dist_km')


def create_threads(functionToThread, grid, poi, numthreads=10):
    """ Splits the grid into n threads to do simultaneous API calls """
    threads = []
    for i in range(numthreads):
        gridpoints = grid[i::numthreads]
        thread = Thread(target=process_grid_sample,
                        args=(functionToThread, gridpoints, poi))
        threads.append(thread)

    # Start each thread, and wait for them to finish before continuing
    [t.start() for t in threads]
    [t.join() for t in threads]


def process_grid_sample(functionToThread, grid_sample, poi):
    """ Given a  sample of the grid, this
    calculates the nearest place to each point"""
    for gridpoint in grid_sample:
        functionToThread(gridpoint[0], gridpoint[1], poi)


def output_nearest_place(latitude, longitude, poi):
    """ Given a lat, long and place of interest,
    it prints the nearest place """
    curr_location = str(latitude) + "," + str(longitude)

    incrementm = distance_on_unit_sphere(increment, 0, 0, 0)
    search_radius = str(int(ceil(sqrt(incrementm**2/2)*1000)))

    url = "https://maps.googleapis.com/maps/api"
    url += "/place/search/json?location="
    url += curr_location + "&sensor=false&key="
    url += GOOGLE_API_KEY + "&radius=" + search_radius + "&types=" + poi

    # Ping the API, and take a break if Google is angry
    while True:
        try:
            response = requests.get(url)
            break
        except requests.ConnectionError:
            time.sleep(randrange(3, 9))

    d = response.json()

    # Output the nearest grocery store
    if len(d['results']) > 0:

        least_miles = 999999999
        for g in d['results']:
            near_lat = g['geometry']['location']['lat']
            near_lng = g['geometry']['location']['lng']
            dist_miles = (distance_on_unit_sphere(latitude,
                          longitude, near_lat, near_lng))
            if dist_miles < least_miles:
                least_miles = dist_miles
                nearest_lat = near_lat
                nearest_lng = near_lng
        # Prevents issues with file writing
        print_lock.acquire()
        try:
            print(poi + ',' + curr_location + ','
                  + str(nearest_lat) + ',' + str(nearest_lng)
                  + ',' + str(least_miles))
        finally:
            print_lock.release()
    # Or, no location found
    else:
        print_lock.acquire()
        try:
            print(poi + ',' + curr_location + ',,,')
        finally:
            print_lock.release()


if scan_type == "grid":
    # New Brunswick
    # lat_NW = 47.939968
    # lng_NW = -69.049870
    # lat_SE = 45.190144
    # lng_SE = -64.270501

    # Canada
    # lat_NW = 83.2911
    # lng_NW = -140.920514
    # lat_SE = 42.016722
    # lng_SE = -52.524864

    # USA
    # lat_NW = 49.44098806129775
    # lng_NW = -127.13476612499217
    # lat_SE = 23.725012
    # lng_SE = -61.347656

    # Fredericton
    lat_NW = 45.998931
    lng_NW = -66.748867
    lat_SE = 45.870202
    lng_SE = -66.550709

    # Gets the grid of points in the area to check
    area_grid = create_area_grid(lat_NW, lng_NW, lat_SE, lng_SE, increment)

    # Has the grid split up into threads and processed
    for place in places:
        create_threads(output_nearest_place, area_grid, place, numthreads=10)
else:
    # List of city centroids
    cities = cities_list(list_name)
    # Has the grid split up into threads and processed
    for place in places:
        create_threads(output_nearest_place, cities, place, numthreads=10)

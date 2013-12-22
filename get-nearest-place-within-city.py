# This scans the entire country for various
# types of places and retrieves the nearest
# one to a grid of points.

import time
import requests
from createcitieslist import cities_list
from progressbar import Percentage, Bar, ProgressBar, \
    ETA
from distancesphere import distance_on_unit_sphere
from threading import Lock
from random import randrange
from math import sqrt, ceil
from createthreads import create_threads
from googleapikey import GOOGLE_API_KEY

# Used to prevent file write issues later
print_lock = Lock()

# Fredericton
lat_NW = 45.998931
lng_NW = -66.748867
lat_SE = 45.870202
lng_SE = -66.550709

# Grid size
increment = 0.0035961575091  # 400 m
incrementm = distance_on_unit_sphere(increment, 0, 0, 0)
search_radius = str(int(ceil(sqrt(incrementm**2/2)*1000)))

# Select which places of interest you'd like to
# scan.

# places = ['grocery_or_supermarket', 'art_gallery', 'library']
# places = ['art_gallery', 'library']
places = ['grocery_or_supermarket', 'hospital', 'art_gallery', 'library']

# Print CSV header
print('place, lat, lng, latnear, lngnear, dist_km')


def output_nearest_place(latitude, longitude, poi):
    """ Given a lat, long and place of interest,
    it prints the nearest place """
    curr_location = str(latitude) + "," + str(longitude)
    global progress

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

        least_km = 999999999
        for g in d['results']:
            near_lat = g['geometry']['location']['lat']
            near_lng = g['geometry']['location']['lng']
            dist_km = (distance_on_unit_sphere(latitude,
                       longitude, near_lat, near_lng))
            if dist_km < least_km:
                least_km = dist_km
                nearest_lat = near_lat
                nearest_lng = near_lng
        # Prevents issues with file writing
        print_lock.acquire()
        try:
            print(poi + ',' + curr_location + ','
                  + str(nearest_lat) + ',' + str(nearest_lng)
                  + ',' + str(least_km))
            progress += 1
            progress_bar.update(progress)
        finally:
            print_lock.release()
    # Or, no location found
    else:
        print_lock.acquire()
        try:
            print(poi + ',' + curr_location + ',,,')
            progress += 1
            progress_bar.update(progress)
        finally:
            print_lock.release()

# I got my centroid list from here: http://geocoder.ca/?freedata=1
cities = cities_list("library/geodata/canada_cities.csv")

progress_bar = (ProgressBar(widgets=[Percentage(), Bar(),
                ETA()], maxval=(len(cities)*len(places))).start())
progress = 0

# Has the grid split up into threads and processed
for place in places:
    create_threads(output_nearest_place, cities, place, numthreads=10)

progress_bar.finish()

import time
from random import randrange
from googleapikey import GOOGLE_API_KEY
import requests
from distancesphere import distance_on_unit_sphere
from math import sqrt, ceil


def output_nearest_place(latitude, longitude, poi, lock,
                         increment=0.2697118131790):
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
        lock.acquire()
        try:
            print(poi + ',' + curr_location + ','
                  + str(nearest_lat) + ',' + str(nearest_lng)
                  + ',' + str(least_miles))
        finally:
            lock.release()
    # Or, no location found
    else:
        lock.acquire()
        try:
            print(poi + ',' + curr_location + ',,,')
        finally:
            lock.release()

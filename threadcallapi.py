import requests
import time
from random import randrange
from threading import Thread, Lock
from googleapikey import GOOGLE_API_KEY
from distancesphere import distance_on_unit_sphere
from progressbar import Percentage, Bar, ProgressBar, \
    ETA

# Used to prevent file write issues
print_lock = Lock()
progress = 0


def process_places(cities, places):
    global progress_bar
    progress_bar = (ProgressBar(widgets=[Percentage(), Bar(),
                    ETA()], maxval=(len(cities)*len(places))).start())
    for place in places:
        create_threads(10, cities, place)


def create_threads(numthreads, cities, poi):
    """ Splits the cities into n threads to do simultaneous API calls """
    threads = []
    for i in range(numthreads):
        city_points = cities[i::numthreads]
        thread = Thread(target=process_city_sample, args=(city_points, poi))
        threads.append(thread)

    # Start each thread, and wait for them to finish before continuing
    [t.start() for t in threads]
    [t.join() for t in threads]
    global progress_bar
    progress_bar.finish()


def process_city_sample(city_sample, poi):
    """ Given a  sample of cities, this
    calculates the nearest place to each point"""
    for city in city_sample:
        output_nearest_place(city[0], city[1], poi)


def output_nearest_place(latitude, longitude, poi):
    """ Given a lat, long and place of interest,
    it prints the nearest place """
    curr_location = str(latitude) + "," + str(longitude)
    global progress

    # 28-mile search radius, which guarantees
    # coverage of a rectangular grid by circles
    url = "https://maps.googleapis.com/maps/api"
    url += "/place/search/json?location="
    url += curr_location + "&sensor=false&key="
    url += GOOGLE_API_KEY + "&radius=46000&types=" + poi

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
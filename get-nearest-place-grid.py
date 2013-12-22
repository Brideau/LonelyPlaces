# This scans the entire country for various
# types of places and retrieves the nearest
# one to a grid of points.

import time
import requests
from progressbar import Percentage, Bar, ProgressBar, \
    ETA
from distancesphere import distance_on_unit_sphere
from random import randrange
from creategrid import create_area_grid
from threading import Lock
from createthreads import create_threads
from googleapikey import GOOGLE_API_KEY

# Prevents write issues from threading
print_lock = Lock()

# New Brunswick
# lat_NW = 47.939968
# lng_NW = -69.049870
# lat_SE = 45.190144
# lng_SE = -64.270501

# Canada
lat_NW = 83.2911
lng_NW = -140.920514
lat_SE = 42.016722
lng_SE = -52.524864

# USA
# lat_NW = 49.44098806129775
# lng_NW = -127.13476612499217
# lat_SE = 23.725012
# lng_SE = -61.347656

# Select which places of interest you'd like to
# scan. Note that for areas with a large land
# mass like Canada, you may go over Google's
# 100,000 daily API call limit if you scan too
# many at once.

# places = ['grocery_or_supermarket', 'art_gallery', 'library']
# places = ['art_gallery', 'library']
# places = ['grocery_or_supermarket', 'hospital', 'art_gallery']

places = ['grocery_or_supermarket', 'library']

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
    url += GOOGLE_API_KEY + "&radius=23000&types=" + poi

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


# Gets the grid of points in the area to check
area_grid = create_area_grid(lat_NW, lng_NW, lat_SE, lng_SE)

progress_bar = (ProgressBar(widgets=[Percentage(), Bar(),
                ETA()], maxval=(len(area_grid)*len(places))).start())
progress = 0

# Has the grid split up into threads and processed
for place in places:
    create_threads(output_nearest_place, area_grid, place, numthreads=10)

progress_bar.finish()

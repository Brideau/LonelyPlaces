# This scans the entire country for various types of places and retrieves the 
# nearest one to a grid of points.

import urllib2, time, requests
from distancesphere import distance_on_unit_sphere
from threading import Thread, Lock
from random import randrange

from googleapikey import GOOGLE_API_KEY

# Used to prevent file write issues later
print_lock = Lock()

# New Brunswick
# lat_NW = 47.939968
# lng_NW = -69.049870
# lat_SE = 45.190144
# lng_SE = -64.270501

# Fredericton
# lat_NW = 45.998931
# lng_NW = -66.748867
# lat_SE = 45.870202
# lng_SE = -66.550709

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

# Select which places of interest you'd like to scan. Note that for areas with a 
# large land mass like Canada, you may go over Google's 100,000 daily API call limit 
# if you scan too many at once.

# places = [ 'grocery_or_supermarket', 'art_gallery', 'library' ]
# places = ['art_gallery', 'library' ]
# places = [ 'grocery_or_supermarket', 'hospital', 'art_gallery' ]

places = [ 'art_gallery', 'hospital']

# Print CSV header
print 'place, lat, lng, latnear, lngnear, dist_miles'

def output_nearest_place(latitude, longitude, poi):
    """ Given a lat, long and place of interest, it 
    prints the nearest place """
    curr_location = str(latitude) + "," + str(longitude)

    # 28-mile search radius, which guarantees coverage of a rectangular grid by circles
    url = 'https://maps.googleapis.com/maps/api/place/search/json?location=' + curr_location + '&sensor=false&key=' + GOOGLE_API_KEY + '&radius=46000&types=' + poi

    # Ping the API, and take a break if Google is angry
    while True:
        try:
            response = requests.get(url)
            break
        except requests.ConnectionError:
            time.sleep(randrange(3,9))
    
    d = response.json()

    # Output the nearest grocery store
    if len(d['results']) > 0:

        least_miles = 999999999
        for g in d['results']:
            near_lat = g['geometry']['location']['lat']
            near_lng = g['geometry']['location']['lng']
            dist_miles = distance_on_unit_sphere(latitude, longitude, near_lat, near_lng)
            if dist_miles < least_miles:
                least_miles = dist_miles
                nearest_lat = near_lat
                nearest_lng = near_lng
        # Prevents issues with file writing
        print_lock.acquire()
        try:
            print poi + ',' + curr_location + ',' + str(nearest_lat) + ',' + str(nearest_lng) + ',' + str(least_miles)
        finally:
            print_lock.release()
    # Or, no location found
    else:
        print_lock.acquire()
        try:
            print poi + ',' + curr_location + ',,,'
        finally:
            print_lock.release()

def process_grid_sample(grid_sample, poi):
    """ Given a  sample of the grid, this calculates the nearest place to each point"""
    for gridpoint in grid_sample:
        output_nearest_place(gridpoint[0], gridpoint[1], poi)

def create_threads(numthreads, grid, poi):
    """ Splits the grid into n threads to do simultaneous API calls """
    threads = []
    for i in range(numthreads):
        gridpoints = grid[i::numthreads]
        thread = Thread(target=process_grid_sample, args=(gridpoints, poi))
        threads.append(thread)

    # Start each thread, and wait for them to finish before continuing
    [ t.start() for t in threads ]
    [ t.join() for t in threads ]


def create_area_grid(start_lat, start_lng, end_lat, end_lng):
    """ Creates a grid that covers the area of interest """
    grid = []

    # About 20 miles distance_on_unit_sphere(0.29, 0, 0, 0)
    lat_incr = -.29
    lng_incr = .29

    # Start in the NW and iterate to the SE. Set to last scanned point if the connection breaks before the scan is finished.
    lat_curr = start_lat
    lng_curr = start_lng

    # Handles the up-down scan
    while lat_curr > end_lat:

        # Resets longitude after each left-right scan
        lng_curr = start_lng

        while lng_curr < end_lng:

            gridpoint = lat_curr, lng_curr
            grid.append(gridpoint)

            # Increments the longitude
            lng_curr += lng_incr

        # Increments the latitude
        lat_curr += lat_incr
    return grid

# Gets the grid of points in the area to check
area_grid = create_area_grid(lat_NW, lng_NW, lat_SE, lng_SE)

# Has the grid split up into threads and processed
for place in places:
    create_threads(10, area_grid, place)

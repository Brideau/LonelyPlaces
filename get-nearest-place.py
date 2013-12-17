# This scans the entire country for various types of places and retrieves the 
# nearest one to a grid of points.

import urllib2, simplejson, time
from distancesphere import distance_on_unit_sphere
from googleapikey import GOOGLE_API_KEY

# API Test
lat_NW = 46.289301
lng_NW = -67.296284
lat_SE = 45.688815
lng_SE = -66.081905

# Canada's country corners
# lat_NW = 83.2911
# lng_NW = -140.920514
# lat_SE = 42.016722
# lng_SE = -52.524864

# USA's country corners
# lat_NW = 49.44098806129775
# lng_NW = -127.13476612499217
# lat_SE = 23.725012
# lng_SE = -61.347656

# About 20 miles distance_on_unit_sphere(0.29, 0, 0, 0)
lat_incr = -.29
lng_incr = .29

# Start in the NW and iterate to the SE. Set to last scanned point if the connection breaks before the scan is finished.
lat_curr = lat_NW
lng_curr = lng_NW
total_calls = 0

# Select which places of interest you'd like to scan. Note that for areas with a 
# large land mass like Canada, you may go over Google's 100,000 daily API call limit 
# if you scan too many at once.

# places = [ 'grocery_or_supermarket', 'art_gallery', 'library' ]
# places = ['art_gallery', 'library' ]
places = [ 'grocery_or_supermarket', 'hospital', 'art_gallery' ]

# Print CSV header
print 'place, lat, lng, latnear, lngnear, dist_miles'

def output_nearest_place(latitude, longitude, poi):
    """ Given a lat, long and place of interest, it 
    prints the nearest place """
    global total_calls
    curr_location = str(latitude) + "," + str(longitude)

    # 28-mile search radius, which guarantees coverage of a rectangular grid by circles
    url = 'https://maps.googleapis.com/maps/api/place/search/json?location=' + curr_location + '&sensor=false&key=' + GOOGLE_API_KEY + '&radius=46000&types=' + poi

    # Ping the API
    response = urllib2.urlopen(url)
    result = response.read()
    d = simplejson.loads(result)
    total_calls += 1

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
        print poi + ',' + curr_location + ',' + str(nearest_lat) + ',' + str(nearest_lng) + ',' + str(least_miles)
    # Or, no location found
    else:
        print poi + ',' + curr_location + ',,,'


for place in places:
    # Handles the up-down scan
    while lat_curr > lat_SE:

        # Resets longitude after each left-right scan
        lng_curr = lng_NW

        while lng_curr < lng_SE:

            output_nearest_place(lat_curr, lng_curr, place)

            # Increments the longitude
            lng_curr += lng_incr

        # Increments the latitude
        lat_curr += lat_incr
    lat_curr = lat_NW
    lng_curr = lng_NW
print total_calls
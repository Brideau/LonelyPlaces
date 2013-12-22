# This scans the entire country for various
# types of places and retrieves the nearest
# one to a grid of points.

from outputnearest import output_nearest_place
from generatesearchlocations import create_area_grid
from threading import Lock
from createthreads import create_threads

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

# Gets the grid of points in the area to check
area_grid = create_area_grid(lat_NW, lng_NW, lat_SE, lng_SE)

# Has the grid split up into threads and processed
for place in places:
    create_threads(output_nearest_place, area_grid, place,
                   print_lock, numthreads=10)

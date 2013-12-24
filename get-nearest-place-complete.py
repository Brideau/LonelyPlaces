# This returns a CSV of the closest place to every point on the grid

import MySQLdb
from distancesphere import distance_on_unit_sphere
from generatesearchlocations import cities_list, create_buildings_list, \
    create_area_grid

placetype = "recycling"
database = "Fredericton"
gridsize = "small"  # "small" / "large"
scantype = "build_list"  # "grid" / "city_list" / "build_list"
if (scantype == "build_list") or (scantype == "city_list"):
    listname = 'library/geodata/locations.csv'

approx_longitude = 49  # Used for distance approximation later

db = (MySQLdb.connect(
      host="127.0.0.1",
      port=8889,
      user="root",
      passwd="root",
      db=database))
c = db.cursor()

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

# Fredericton
# lat_NW = 45.998931
# lng_NW = -66.748867
# lat_SE = 45.870202
# lng_SE = -66.550709

if gridsize == "small":
    incr = 0.0035961575091
else:
    incr = .2697118131790

# Start in the northwest and iterate to the southeast
print("lat,lng,latnear,lngnear,dist_km")

lat_dist = str(distance_on_unit_sphere(1, 0, 0, 0))
lng_dist = str(distance_on_unit_sphere(approx_longitude, 1,
               approx_longitude, 0))

if scantype == "grid":
    locations = create_area_grid(lat_NW, lng_NW, lat_SE,
                                 lng_SE, increment=incr)
elif scantype == "city_list":
    locations = cities_list(listname)
else:
    locations = create_buildings_list(listname)

for location in locations:
    # Equirectangular approximation at 49th parallel:
    # http://www.movable-type.co.uk/scripts/latlong.html
    sql = "SELECT latitude, longitude,SQRT(POW(" + lat_dist + " * ("
    sql += "latitude - " + str(location[0]) + "), 2) + "
    sql += "POW(" + lat_dist + " * (" + str(location[1]) + " - longitude) "
    sql += "* COS(latitude / " + lng_dist + "), 2)) AS distance FROM "
    sql += "`" + placetype + "` ORDER BY distance LIMIT 0,1"
    c.execute(sql)
    result = c.fetchall()[0]
    curr_location = str(location[0]) + "," + str(location[1])
    nearest_lat = result[0]
    nearest_lng = result[1]
    kilometres = result[2]
    print(curr_location + ',' + str(nearest_lat) + ','
          + str(nearest_lng) + ',' + str(kilometres))

# This returns a CSV of the closest place to every point on the grid

import MySQLdb
db = (MySQLdb.connect(
      host="127.0.0.1",
      port=8889,
      user="root",
      passwd="root",
      db="can_hosp"))
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

# About 20 miles
lat_incr = -.29
lng_incr = .29

# Start in the northwest and iterate to the southeast
lat_curr = lat_NW
lng_curr = lng_NW
print("lat,lng,latnear,lngnear,dist_miles")

while lat_curr > lat_SE:
    lng_curr = lng_NW
    while lng_curr < lng_SE:
        # distance_on_unit_sphere(1, 0, 0, 0) = 69.1
        # Equirectangular approximation:
        # http://www.movable-type.co.uk/scripts/latlong.html
        sql = "SELECT latitude, longitude,SQRT(POW(69.1 * ("
        sql += "latitude - " + str(lat_curr) + "), 2) + "
        sql += "POW(69.1 * (" + str(lng_curr) + " - longitude) "
        sql += "* COS(latitude / 57.3), 2)) AS distance FROM "
        sql += "`hospital` ORDER BY distance LIMIT 0,1"
        c.execute(sql)
        result = c.fetchall()[0]
        curr_location = str(lat_curr) + "," + str(lng_curr)
        nearest_lat = result[0]
        nearest_lng = result[1]
        miles = result[2]
        print(curr_location + ',' + str(nearest_lat) + ','
              + str(nearest_lng) + ',' + str(miles))
        lng_curr += lng_incr
    lat_curr += lat_incr

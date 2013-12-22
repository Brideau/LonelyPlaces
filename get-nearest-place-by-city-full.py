# This returns a CSV of the closest place to every point on the grid

import MySQLdb
from generatesearchlocations import cities_list

db = (MySQLdb.connect(
      host="127.0.0.1",
      port=8889,
      user="root",
      passwd="root",
      db="can_lib_city"))
c = db.cursor()

cities = cities_list("library/geodata/canada_cities.csv")

print("lat,lng,latnear,lngnear,dist_km")


for city in cities:
    # distance_on_unit_sphere(1, 0, 0, 0) = 111.30
    # Equirectangular approximation:
    # http://www.movable-type.co.uk/scripts/latlong.html
    sql = "SELECT latitude, longitude,SQRT(POW(111.30 * ("
    sql += "latitude - " + str(city[0]) + "), 2) + "
    sql += "POW(111.30 * (" + str(city[1]) + " - longitude) "
    sql += "* COS(latitude / 72.97), 2)) AS distance FROM "
    sql += "`library` ORDER BY distance LIMIT 0,1"
    c.execute(sql)
    result = c.fetchall()[0]
    curr_location = str(city[0]) + "," + str(city[1])
    nearest_lat = result[0]
    nearest_lng = result[1]
    kilometres = result[2]
    print(curr_location + ',' + str(nearest_lat) + ','
          + str(nearest_lng) + ',' + str(kilometres))

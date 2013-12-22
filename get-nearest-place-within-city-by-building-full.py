# This returns a CSV of the closest place to every point on the grid

import MySQLdb
from generatesearchlocations import create_buildings_list

db = (MySQLdb.connect(
      host="127.0.0.1",
      port=8889,
      user="root",
      passwd="root",
      db="fred_grocery"))
c = db.cursor()

building_list = create_buildings_list('library/geodata/locations.csv')

print("lat,lng,latnear,lngnear,dist_km")

for building in building_list:
    # distance_on_unit_sphere(1, 0, 0, 0) = 111.30
    # Equirectangular approximation at 49th parallel:
    # http://www.movable-type.co.uk/scripts/latlong.html
    sql = "SELECT latitude, longitude,SQRT(POW(111.30 * ("
    sql += "latitude - " + str(building[0]) + "), 2) + "
    sql += "POW(111.30 * (" + str(building[1]) + " - longitude) "
    sql += "* COS(latitude / 72.97), 2)) AS distance FROM "
    sql += "`grocery` ORDER BY distance LIMIT 0,1"
    c.execute(sql)
    result = c.fetchall()[0]
    curr_location = str(building[0]) + "," + str(building[1])
    nearest_lat = result[0]
    nearest_lng = result[1]
    kilometres = result[2]
    print(curr_location + ',' + str(nearest_lat) + ','
          + str(nearest_lng) + ',' + str(kilometres))

# This returns a CSV of the closest place to every point on the grid

import MySQLdb
from createcitieslist import cities_list
from progressbar import Percentage, Bar, ProgressBar, \
    ETA

db = (MySQLdb.connect(
      host="127.0.0.1",
      port=8889,
      user="root",
      passwd="root",
      db="can_lib_city"))
c = db.cursor()

cities = cities_list("library/geodata/canada_cities.csv")

progress_bar = (ProgressBar(widgets=[Percentage(), Bar(),
                ETA()], maxval=len(cities)).start())
progress = 0

print("lat,lng,latnear,lngnear,dist_km")


for city in cities:
    progress += 1
    progress_bar.update(progress)
    # distance_on_unit_sphere(1, 0, 0, 0) = 69.1
    # Equirectangular approximation:
    # http://www.movable-type.co.uk/scripts/latlong.html
    sql = "SELECT latitude, longitude,SQRT(POW(69.1 * ("
    sql += "latitude - " + str(city[0]) + "), 2) + "
    sql += "POW(69.1 * (" + str(city[1]) + " - longitude) "
    sql += "* COS(latitude / 57.3), 2)) AS distance FROM "
    sql += "`library` ORDER BY distance LIMIT 0,1"
    c.execute(sql)
    result = c.fetchall()[0]
    curr_location = str(city[0]) + "," + str(city[1])
    nearest_lat = result[0]
    nearest_lng = result[1]
    kilometres = result[2]
    print(curr_location + ',' + str(nearest_lat) + ','
          + str(nearest_lng) + ',' + str(kilometres))

progress_bar.finish()

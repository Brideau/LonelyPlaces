# This returns a CSV of the closest place to every point on the grid

import MySQLdb
from creategrid import create_area_grid

db = (MySQLdb.connect(
      host="127.0.0.1",
      port=8889,
      user="root",
      passwd="root",
      db="fred_grocery"))
c = db.cursor()

# Fredericton
lat_NW = 45.998931
lng_NW = -66.748867
lat_SE = 45.870202
lng_SE = -66.550709

# Grid size
increment = 0.0035961575091  # 400 m

area_grid = create_area_grid(lat_NW, lng_NW, lat_SE,
                             lng_SE, increment=increment)

print("lat,lng,latnear,lngnear,dist_km")

for gridpoint in area_grid:
    # distance_on_unit_sphere(1, 0, 0, 0) = 111.30
    # Equirectangular approximation at 49th parallel:
    # http://www.movable-type.co.uk/scripts/latlong.html
    sql = "SELECT latitude, longitude,SQRT(POW(111.30 * ("
    sql += "latitude - " + str(gridpoint[0]) + "), 2) + "
    sql += "POW(111.30 * (" + str(gridpoint[1]) + " - longitude) "
    sql += "* COS(latitude / 72.97), 2)) AS distance FROM "
    sql += "`grocery` ORDER BY distance LIMIT 0,1"
    c.execute(sql)
    result = c.fetchall()[0]
    curr_location = str(gridpoint[0]) + "," + str(gridpoint[1])
    nearest_lat = result[0]
    nearest_lng = result[1]
    kilometres = result[2]
    print(curr_location + ',' + str(nearest_lat) + ','
          + str(nearest_lng) + ',' + str(kilometres))

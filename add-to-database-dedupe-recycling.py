# This takes the retrieved data from import-grocery.py and sends the place
# locations into a database, and dedupes any accidental duplicates.

import MySQLdb
from generatesearchlocations import create_recycling_list

db = (MySQLdb.connect(
      host="127.0.0.1",
      port=8889,
      user="root",
      passwd="root",
      db="Fredericton"))

c = db.cursor()

# If you did a scan by city, run once for each cleaned file from
# get-nearest-place-by-city and get-nearest-place-grid
filename = 'library/geodata/FrederictonRecycling.csv'
reader = create_recycling_list(filename)

skipped_header = False
for row in reader:
    # If no result from Google
    if row[0] == '' or row[1] == '':
        continue

    # Only add unique locations
    query = ("SELECT * FROM `recycling` WHERE `latitude` = '"
             + str(row[0]) + "' AND `longitude` = '"
             + str(row[1]) + "'")
    c.execute(query)
    if len(c.fetchall()) > 0:
        continue

    sql = ("INSERT INTO `recycling` (latitude, longitude) VALUES ("
           + "'" + str(row[0]) + "','" + str(row[1]) + "'" + ")")
    c.execute(sql)

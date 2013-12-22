# This takes the retrieved data from import-grocery.py and sends the place
# locations into a database, and dedupes any accidental duplicates.

import MySQLdb
import csv

db = (MySQLdb.connect(
      host="127.0.0.1",
      port=8889,
      user="root",
      passwd="root",
      db="can_groc"))

c = db.cursor()

# If you did a scan by city, run once for each cleaned file from
# get-nearest-place-by-city and get-nearest-place-grid
filename = '_CanadaData/CanadaLibrary.csv'
reader = csv.reader(open(filename, 'rb'), delimiter=',')

skipped_header = False
for row in reader:
    # Skips the first line of each file
    if not skipped_header:
        skipped_header = True
        continue

    # If no result from Google
    if row[2] == '' or row[3] == '':
        continue

    # Only add unique locations
    query = ("SELECT * FROM `grocery` WHERE `latitude` = '"
             + str(row[2]) + "' AND `longitude` = '"
             + str(row[3]) + "'")
    c.execute(query)
    if len(c.fetchall()) > 0:
        continue

    sql = ("INSERT INTO `grocery` (latitude, longitude) VALUES ("
           + "'" + str(row[2]) + "','" + str(row[3]) + "'" + ")")
    c.execute(sql)

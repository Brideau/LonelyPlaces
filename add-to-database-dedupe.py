# This takes the retrieved data from import-grocery.py and sends the place
# locations into a database, and dedupes any accidental duplicates.

import MySQLdb
import csv
from generatesearchlocations import create_recycling_list

placetype = "grocery"
database = "Fredericton"
listtype = "standard"  # "standard" / "custom"
filename = '_CanadaData/FrederictonGrocery.csv'

db = (MySQLdb.connect(
      host="127.0.0.1",
      port=8889,
      user="root",
      passwd="root",
      db=database))

c = db.cursor()

# Create the database table
sql = "CREATE TABLE IF NOT EXISTS `" + placetype + "` ("
sql += "`id` int(11) NOT NULL auto_increment,"
sql += "`latitude` decimal(10,7) NOT NULL,"
sql += "`longitude` decimal(10,7) NOT NULL,"
sql += "PRIMARY KEY  (`id`)"
sql += ") ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;"

c.execute(sql)

# If you did a scan by city, run once for each cleaned file from
# get-nearest-place-by-city and get-nearest-place-grid
if listtype == "standard":
    reader = csv.reader(open(filename, 'rb'), delimiter=',')
else:
    reader = create_recycling_list(filename)

if listtype == "standard":
    col1 = 2
    col2 = 3
else:
    col1 = 0
    col2 = 1

skipped_header = False
for row in reader:
    # Skips the first line of each file
    if not skipped_header:
        skipped_header = True
        continue

    # If no result from Google
    if row[col1] == '' or row[col2] == '':
        continue

    # Only add unique locations
    query = ("SELECT * FROM `" + placetype + "` WHERE `latitude` = '"
             + str(row[col1]) + "' AND `longitude` = '"
             + str(row[col2]) + "'")
    c.execute(query)
    if len(c.fetchall()) > 0:
        continue

    sql = ("INSERT INTO `" + placetype + "` (latitude, longitude) VALUES ("
           + "'" + str(row[col1]) + "','" + str(row[col2]) + "'" + ")")
    c.execute(sql)

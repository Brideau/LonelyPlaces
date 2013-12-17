# Used when you're running the can over multiple place types
# to separate the data into different files.

import csv

placeType = "art_gallery"

print "place, lat, lng, latnear, lngnear, dist_miles"

for i in range(1,5):
    filename = 'nearest-GrocArtHospCAN' + str(i) + '.csv'
    reader = csv.reader(open(filename, 'rb'), delimiter=',')
    skipped_header = False
    for row in reader:
        # Skips the first line of each file
        if not skipped_header:
            skipped_header = True
            continue

        if str(row[0]) == placeType:
            print row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5]
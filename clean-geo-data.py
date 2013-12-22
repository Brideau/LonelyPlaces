# Used when you're running the scan over multiple place
# types to separate the data into different files.

import csv

placeType = "art_gallery"

print("lat, lng, latnear, lngnear, dist_km")

# Use when you have more than one file that needs to be combined
# for i in range(1, 5):
#     filename = 'nearest-GrocArtHospCAN' + str(i) + '.csv'
#     reader = csv.reader(open(filename, 'rb'), delimiter=',')
#     skipped_header = False
#     for row in reader:
#         # Skips the first line of each file
#         if not skipped_header:
#             skipped_header = True
#             continue

#         if str(row[0]) == placeType:
#             print(row[1] + ',' + row[2] + ',' + row[3]
#                   + ',' + row[4] + ',' + row[5])

# Use when you only have one file that contains more than one place of interest
file = 'NearestPlacesByCity.csv'
reader = csv.reader(open(file, 'rb'), delimiter=',')
skipped_header = False
for row in reader:
    # Skips the first line of each file
    if not skipped_header:
        skipped_header = True
        continue

    if str(row[0]) == placeType:
        print(row[1] + ',' + row[2] + ',' + row[3]
              + ',' + row[4] + ',' + row[5])

Lonely Places
===============

![](http://www.ryanbrideau.com/dataviz/deserts/CanadaHospitalGrid.png)

NOTE: Lots more documentation needed.

Extracts location data about various place types from Google Places, and produces a line map showing how close a grid of locations are from these places.

Run in the following order, making adjustments to the variables at the top of each file to suit your needs:

1. **get-nearest-place.py**: Scans the entire area you're looking at and records the location of the nearest place of interest.
2. **clean-geo-data.py**: Separates data into separate files if you run the Google Places scan using multiple "place types"
3. **add-to-database-dedupe.py**: Imports your place data into a MySQL database and de-duplicates any place locations.
4. **get-nearest-place-complete.py**: Finds the nearest location of interest for every point on a grid. Uses data in MySQL database and outputs a CSV.
5. **map-places.R**: Maps the data produced in step 4.

Others:
**distancehistogram.R**: Used to create a histogram of the distances for extra insight
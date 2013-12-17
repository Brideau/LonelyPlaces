CanadianDeserts
===============

Extracts location data about various place types from Google Places, and produces a line map showing how close a grid of locations are from these places.

Run in the following order:

1. **get-nearest-place.py**: Scans the entire area you're looking for and records the location of the nearest place of interest. Produces a CSV.
2. **clean-geo-data.py**: Separates data into separate files if you run the Google Places scan using multiple "place types"
3. **add-to-database-dedupe.py**: Imports your data into a MySQL database and de-duplicates any places
4. **get-nearet-place-full.py**: Finds the nearest location of interest for every point on a grid. Uses data in MySQL database.
5. **map-places.R**: Maps the data produced in step 4.
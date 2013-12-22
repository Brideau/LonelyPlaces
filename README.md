CanadianDeserts
===============

Extracts location data about various place types from Google Places, and produces a line map showing how close a grid of locations are from these places.

Run in the following order if you want to scan an area with a uniform grid:

1. **get-nearest-place-grid.py**: Scans the entire area you're looking at and records the location of the nearest place of interest.
2. **clean-geo-data.py**: Separates data into separate files if you run the Google Places scan using multiple "place types"
3. **add-to-database-dedupe.py**: Imports your place data into a MySQL database and de-duplicates any place locations (see note below).
4. **get-nearest-place-grid-full.py**: Finds the nearest location of interest for every point on a grid. Uses data in MySQL database and outputs a CSV.
5. **map-places.R**: Maps the data produced in step 4.

Run in the following order if you want to scan an area and have a list of cities:

1. **get-nearest-place-by-city.py**: Takes in a list of cities and finds the nearest place of interest to each one.
2. **get-nearest-place-grid.py**: Scans the entire area you're looking at and records the location of the nearest place of interest to points on a grid. Used to fill in the gaps between cities for remote areas.
2. **clean-geo-data.py**: Separates data into separate files if you run the Google Places scan using multiple "place types"
3. **add-to-database-dedupe.py**: Imports your place data into a MySQL database and de-duplicates any place locations (see note below). This should be run once for each file from steps 1 an 2.
4. **get-nearest-place-by-city-full.py**: Finds the nearest location of interest for every point on a grid. Uses data in MySQL database and outputs a CSV.
5. **map-places.R**: Maps the data produced in step 4.


After creating a database in step 2, use the following MySQL to create the necessary table:

```sql
CREATE TABLE IF NOT EXISTS `grocery` (
  `id` int(11) NOT NULL auto_increment,
  `latitude` decimal(10,7) NOT NULL,
  `longitude` decimal(10,7) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
```
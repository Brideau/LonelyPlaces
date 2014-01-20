import csv
import pyproj

# Specify which towns you want to include by town code number
nb_towns = {'4508': 'Fredericton',
            '4535': 'New Maryland',
            '5010': 'Lincoln',
            '11078': 'Richibucto',
            '5054': 'Maugerville',
            '5053': 'Maugerville',
            '4633': 'Island View',
            '4515': 'Douglas'}
wgs84 = pyproj.Proj("+init=EPSG:4326")  # Used by Google
nb_coords = pyproj.Proj("+init=EPSG:2953")  # EPSG number came with data readme


def cities_list(city_centroid_file):
    """ Generate a city list from a file """
    city_locations = []
    file_reader = csv.reader(open(city_centroid_file, 'rb'), delimiter=',')

    for row in file_reader:
        lat = float(row[2])
        lng = -1*float(row[3])
        city = lat, lng
        city_locations.append(city)

    return city_locations


def create_buildings_list(property_id_list):
    """ Generate a list of building locations from a list """
    file_reader = csv.reader(open(property_id_list, 'rb'), delimiter=',')
    building_locations = []
    skipped_header = False
    for row in file_reader:
        if not skipped_header:
            skipped_header = True
            continue

        try:
            # Modify depending on what column lat/long are stored in
            x_coor = float(row[2])
            y_coor = float(row[3])
        except ValueError:
            continue
        # Change the first argument of this depending on file projection, or
        # switch comments if it's not necessary
        # location = pyproj.transform(nb_coords, wgs84, x_coor, y_coor)

        # building = location[1], location[0]
        building = x_coor, y_coor
        building_locations.append(building)
    return building_locations


def create_recycling_list(property_id_list):
    """ Generate a set of a town list from a file """
    file_reader = csv.reader(open(property_id_list, 'rb'), delimiter=',')
    recycling_locations = []
    skipped_header = False
    for row in file_reader:
        if not skipped_header:
            skipped_header = True
            continue
        try:
            # Checks to see if a point of interest was found
            x_coor = float(row[2])
            y_coor = float(row[3])
        except ValueError:
            continue
        # This cause an issue - spotted what I think was a bug
        # but haven't had a chance to test it. This used to do a
        # coordinate transformation like above, but it was unnecessary.
        # If something breaks, try reversing the coordinates
        depot = x_coor, y_coor
        recycling_locations.append(depot)
    return recycling_locations


def create_list(property_id_list):
    """ Generate a list from a csv file """
    file_reader = csv.reader(open(property_id_list, 'rb'), delimiter=',')
    locations = []
    skipped_header = False
    for row in file_reader:
        if not skipped_header:
            skipped_header = True
            continue
        try:
            x_coor = float(row[5])
            y_coor = float(row[6])
        except ValueError:
            continue
        location = x_coor, y_coor
        locations.append(location)
    return locations


def create_area_grid(start_lat, start_lng, end_lat, end_lng,
                     increment=0.2697118131790):
    """ Creates a grid that covers the area of interest """

    # increment = 0.2697118131790 ~ 30 km
    # increment = 0.0035961575091 ~ 400 m

    grid = []

    # Start in the NW and iterate to the SE. Set to
    # last scanned point if the connection breaks
    # before the scan is finished.
    lat_curr = start_lat
    lng_curr = start_lng

    # Handles the up-down scan
    while lat_curr > end_lat:

        # Resets longitude after each left-right scan
        lng_curr = start_lng

        while lng_curr < end_lng:

            gridpoint = lat_curr, lng_curr
            grid.append(gridpoint)

            # Increments the longitude
            lng_curr += increment

        # Increments the latitude
        lat_curr -= increment
    return grid

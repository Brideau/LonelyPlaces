import csv


def cities_list(city_centroid_file):
    """ Creates a grid that covers the area of interest """
    city_locations = []
    file_reader = csv.reader(open(city_centroid_file, 'rb'), delimiter=',')

    for row in file_reader:
        lat = float(row[2])
        lng = -1*float(row[3])
        city = lat, lng
        city_locations.append(city)

    return city_locations

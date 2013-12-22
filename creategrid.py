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

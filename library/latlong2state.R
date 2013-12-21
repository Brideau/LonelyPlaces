library(sp)
library(rgdal)
library(maptools)
library(raster)

# This function accepts a dataframe with Col 1 being longitude in degrees
# and Col 2 being latitude in degrees.

latlong2state <- function(pointsDF) {
  
  # Load the data downloaded from http://www.gadm.org/
  country.data <- getData('GADM', country="CAN", level = 1)
  # Pull the names out of the data file
  stateNames <- country.data$NAME_1
  country_sp <- SpatialPolygons(country.data@polygons, proj4string=CRS("+proj=longlat +datum=WGS84"))
  
  # Convert pointsDF to a SpatialPoints object
  pointsSP <- SpatialPoints(pointsDF, proj4string=CRS("+proj=longlat +datum=WGS84"))
  
  # Use 'over' to get _indicies_ of the Polygons object containing each point
  indicies <- over(pointsSP, country_sp)
  
  # Return the state names of the Polygons object containing each point
  stateNames[indicies]
}


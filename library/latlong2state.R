library(sp)
library(rgdal)
library(rgeos)
library(maptools)
library(raster)

# This function accepts a dataframe with Col 1 being longitude in degrees
# and Col 2 being latitude in degrees.

latlong2state <- function(pointsDF) {
  
  # Saves the country geo data locally
  localDir <- 'library/geodata'
  if (!file.exists(localDir)) {
    dir.create(localDir)
  }
  # Load the data downloaded from http://www.gadm.org/. Level 1 contains province/state level data.
  country.data <- getData('GADM', country="CAN", level = 1, download=TRUE, path='library/geodata')
  
  # Pull the names out of the data file
  stateNames <- country.data$NAME_1
  country_sp <- SpatialPolygons(country.data@polygons, proj4string=CRS("+proj=longlat +datum=WGS84"))
  
  # Simplify the province data using the Douglas-Peuker algorithm. Results in overall
  # speed increase of 3x, and on Canadian data, only missed 1/20000 points.
  country_sp <- gSimplify(country_sp, tol=0.01, topologyPreserve=TRUE)
  
  # Convert pointsDF to a SpatialPoints object
  pointsSP <- SpatialPoints(pointsDF, proj4string=CRS("+proj=longlat +datum=WGS84"))
  
  # Use 'over' to get _indicies_ of the Polygons object containing each point
  indicies <- over(pointsSP, country_sp)
  
  # Return the state names of the Polygons object containing each point
  stateNames[indicies]
}

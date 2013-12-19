library(sp)
library(maps)
library(maptools)

# This function accepts a dataframe with Col 1 being longitude in degrees
# and Col 2 being latitude in degrees.

latlong2state <- function(pointsDF) {
  # Commented out section applies to the original US data
  # Loads all the spatial polygons for plotting the US States
  
  # states <- map('state', fill=TRUE, col="transparent", plot=FALSE)
  # Get the state names
  # IDs <-sapply(strsplit(states$names, ":"), function(x) x[1])
  # Map states to spatial polygons
  # states_sp <- map2SpatialPolygons(states, IDs = IDs, proj4string=CRS("+proj=longlat +datum=wgs84"))
  
  # Load the data downloaded from http://www.gadm.org/
  load('CanadaGeoData/02Provinces.RData')
  # Pull the names out of the data file
  canIDs <- gadm@data$NAME_1
  prov_sp <- gadm[2]
  
  
  # Convert pointsDF to a SpatialPoints object
  pointsSP <- SpatialPoints(pointsDF, proj4string=CRS("+proj=longlat +datum=wgs84"))
  
  # Use 'over' to get _indicies_ of the Polygons object containing each point
  indicies <- over(pointsSP, prov_sp)
  
  # Return the state names of the Polygons object containing each point
  stateNames <- sapply(states_sp@polygons, function(x) x@ID)
  statesNames[indicies]
}
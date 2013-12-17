library(sp)
library(maps)
library(maptools)

# This function accepts a dataframe with Col 1 being longitude in degrees
# and Col 2 being latitude in degrees.

latlong2state <- function(pointsDF) {
  # Loads all the spatial polygons for plotting the states
  states <- map('state', fill=TRUE, col="transparent", plot=FALSE)
  # Cleans up the state data
  IDs <-sapply(strsplit(states$names, ":"), function(x) x[1])
  states_sp <- map2SpatialPolygons(states, IDs = IDs, proj4string=CRS("+proj=longlat +datum=wgs84"))
  
  # Convert pointsDF to a SpatialPoints object
  pointsSP <- SpatialPoints(pointsDF, proj4string=CRS("+proj=longlat +datum=wgs84"))
  
  # Use 'over' to get _indicies_ of the Polygons object containing each point
  indicies <- over(pointsSP, states_sp)
  
  # Return the state names of the Polygons object containing each point
  stateNames <- sapply(states_sp@polygons, function(x) x@ID)
  statesNames[indicies]
}
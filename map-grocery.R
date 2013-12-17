source('./library/latlong2state.R')

library(maps)
library(mapproj)
library(geosphere)

# Map-specific variables
latFocus = c(39, 45) # (lat0, lat1) where the Albers projection is accurate
lineColours = c("#ffffff", "red")
fileName = "nearest-grocery-fullUS.csv"

getLineColor <- function(val) {
  pal <- colorRampPalette(lineColours)
  colors <- pal(80)
  val.log <- log(val)
  
  if (val > 50) {
    col <- colors[80]
  } else {
    colindex <- max(1, round( 80 * val / 50))
    col <- colors[colindex]
  }
  return(col)
}

# Load the data
location <- read.csv(fileName, stringsAsFactors=FALSE)

# Omit locations that are not on the map of focus
location$state <- latlong2state(data.frame(location$lng, location$lat))
location$nearstate <- latlong2state(data.frame(location$lngnear, location$latnear))
location <- na.omit(location)

# Draw a base map. Albers is true scale at lat0, lat1
map("state", proj="albers", param=latFocus, col="#999999", fill=FALSE, bg="#ffffff", lwd=0.8)

# Plot the grid points
pts0 <- mapproject(unlist(location[, 'lng']), unlist(location[, 'lat']))
pts1 <- mapproject(unlist(location[, 'lngnear']), unlist(location[, 'latnear']))
seg.colors <- sapply(location$dist_miles, FUN=getLineColor)

# Draw the map and line segments
segments(pts0$x, pts0$y, pts1$x, pts1$y, col=seg.colors, lwd=1.2)





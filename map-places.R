source('./library/latlong2state.R')

library(maps)
library(mapproj)
library(mapdata)
library(geosphere)
library(ggmap)

# Map-specific variables
latFocus = c(50, 75) # (lat0, lat1) where the Albers projection is accurate
lineColours = c("#ffffff", "red")
fileName = "_CanadaData/CanadaHospitalComplete.csv"

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
map("worldHires", "Canada", proj="albers", param=latFocus, col="#999999", fill=FALSE, bg="#ffffff", lwd=0.8)

# Plot the grid points
pts0 <- mapproject(unlist(location[, 'lng']), unlist(location[, 'lat']))
pts1 <- mapproject(unlist(location[, 'lngnear']), unlist(location[, 'latnear']))
seg.colors <- sapply(location$dist_miles, FUN=getLineColor)

# Draw the map and line segments
segments(pts0$x, pts0$y, pts1$x, pts1$y, col=seg.colors, lwd=1.2)

stateMap <- function(bbox, thedata) {
  basemap <- get_map(location=bbox, zoom=7, source='google', maptype="roadmap", color="bw")
  ggmap(basemap) + geom_segment(aes(x=lng, xend=lngnear, y=lat, yend=latnear, color=dist_miles), size=0.6, data=thedata) + geom_point(aes(x=lngnear, y=latnear), size=2, color="#000000", border="black", data=thedata) + scale_color_gradient(low="white", high="red", limits=c(0, 80))
}

# montana <- c(-116.23363635500002, 44.11419853862171, -103.48949572999454, 49.349270649782994)
# stateMap(montana, subset(location, state=='montana'))
# 
# nv.ut.ca.az <- c(-124.23168322999285, 31.460280893111246, -108.14769885499943, 42.32097191215088)
# stateMap(nv.ut.ca.az, subset(location, state=='nevada' | state == 'utah' | state == 'california' | state == 'arizona'))

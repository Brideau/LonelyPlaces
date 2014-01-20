source('./library/latlong2state.R')

library(maps)
library(mapproj)
library(mapdata)
library(geosphere)
library(ggmap)

fileName = "_Starbucks/StarbucksListComplete.csv"

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
# Get a subset of the above data based on distances
location.0.6 <- subset(location, dist_km > 0.6)
location.1.00 <- subset(location, dist_km > 1.00)


# Omit locations that are not on the map of focus (not needed for city maps unless they are on a border)
# location$state <- latlong2state(data.frame(location$lng, location$lat))
# location$nearstate <- latlong2state(data.frame(location$lngnear, location$latnear))
location <- na.omit(location)
location.0.6 <- na.omit(location.0.6)
location.1.00 <- na.omit(location.1.00)

createMap <- function(bbox, thedata, mapzoom=3, linesize=0.6, pointsize=2) {
  basemap <- get_map(location=bbox, zoom=mapzoom, source='google', maptype="roadmap", color="color")
  ggmap(basemap) + geom_segment(aes(x=lng, xend=lngnear, y=lat, yend=latnear), colour="#00754f", alpha=0.2, size=linesize, data=thedata) + geom_point(aes(x=lngnear, y=latnear), size=pointsize, color="#00000050", border="black", data=thedata)
}

# Country bounding box c(left, bottom, right, top)
# canada <- c(-140.920514, 42.016722, -52.524864, 83.2911)
# createMap(canada, location, 3)

# new_brunswick <- c(-69.049870, 45.190144, -64.270501, 47.939968)
# createMap(new_brunswick, subset(location, state=='New Brunswick'), mapzoom=7, linesize=0.3, pointsize=1)

# fredericton <- c(-66.748867, 45.870202, -66.550709, 45.998931)
# createMap(fredericton, location, mapzoom=12, linesize=0.5, pointsize=2)

vancouver <- c(-123.240284, 49.194593, -123.005238, 49.299415)
createMap(vancouver, location, mapzoom=12, linesize=0.5, pointsize=2)
createMap(vancouver, location.0.6, mapzoom=12, linesize=1, pointsize=2)
createMap(vancouver, location.1.00, mapzoom=12, linesize=10, pointsize=2)

# You can also submit multiple states at once:
# nv.ut.ca.az <- c(-124.23168322999285, 31.460280893111246, -108.14769885499943, 42.32097191215088)
# createMap(nv.ut.ca.az, subset(location, state=='nevada' | state == 'utah' | state == 'california' | state == 'arizona'))

source('./library/latlong2state.R')

library(maps)
library(mapproj)
library(mapdata)
library(geosphere)
library(ggmap)
library(rgdal)
library(raster)

fileName = "_CanadaData/CanadaHospitalComplete.csv"

getLineColor <- function(val) {
  pal <- colorRampPalette(c("blue", "red"))
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

# Omit locations that are not on the map of focus (not needed for city maps unless they are on a border)
location$state <- latlong2state(data.frame(location$lng, location$lat))
location$nearstate <- latlong2state(data.frame(location$lngnear, location$latnear))
location <- na.omit(location)

# createMap <- function(bbox, thedata, mapzoom=3, linesize=0.6, pointsize=2) {
#   basemap <- get_map(location=bbox, zoom=mapzoom, source='google', maptype="roadmap", color="color")
#   ggmap(basemap) + geom_segment(aes(x=lng, xend=lngnear, y=lat, yend=latnear), colour="#13cf0b", alpha=0.05, size=linesize, data=thedata) + geom_point(aes(x=lngnear, y=latnear), size=pointsize, color="#00000050", border="black", data=thedata)
# }

createMap <- function(bbox, thedata, mapzoom=3, linesize=0.6, pointsize=2) {
  basemap <- get_map(location=bbox, zoom=mapzoom, source='google', maptype="roadmap", color="color")
  ggmap(basemap) + geom_segment(aes(x=lng, xend=lngnear, y=lat, yend=latnear, color=dist_miles), size=0.6, data=thedata) + geom_point(aes(x=lngnear, y=latnear), size=2, color="#000000", border="black", data=thedata) + scale_color_gradient(low="blue", high="red", limits=c(0, max(thedata$dist_miles)))
}

pts0 <- mapproject(unlist(location[, 'lng']), unlist(location[, 'lat']))
pts1 <- mapproject(unlist(location[, 'lngnear']), unlist(location[, 'latnear']))
seg.colors <- sapply(location$dist_miles, FUN=getLineColor)

# Saves the country geo data locally
localDir <- 'library/geodata'
if (!file.exists(localDir)) {
  dir.create(localDir)
}

canada.data <- getData('GADM', country="CAN", level = 1, download=TRUE, path='library/geodata')
canada.data <- gSimplify(canada.data, tol=0.01, topologyPreserve=TRUE)

# canada.map <- readOGR(shapefile.dir, "prov_ab_p_geo83_e")
canada.data.trans <- spTransform(canada.data, CRS("+proj=ortho +ellps=WGS84"))

plot(canada.data)

plot(canada.map, border="#CCCCCC")
segments(pts0$x, pts0$y, pts1$x, pts1$y, col=seg.colors, lwd=0.8)


# Country bounding box c(left, bottom, right, top)
canada <- c(-140.920514, 42.016722, -52.524864, 83.2911)
createMap(canada, location)

# new_brunswick <- c(-69.049870, 45.190144, -64.270501, 47.939968)
# createMap(new_brunswick, subset(location, state=='New Brunswick'), mapzoom=7, linesize=0.3, pointsize=1)

# fredericton <- c(-66.748867, 45.870202, -66.550709, 45.998931)
# createMap(fredericton, location, mapzoom=12, linesize=0.5, pointsize=2)

# You can also submit multiple states at once:
# nv.ut.ca.az <- c(-124.23168322999285, 31.460280893111246, -108.14769885499943, 42.32097191215088)
# createMap(nv.ut.ca.az, subset(location, state=='nevada' | state == 'utah' | state == 'california' | state == 'arizona'))

library(ggplot2)

# Create a distance histogram
histogram <- ggplot(location.1.00, aes(x=dist_km)) + geom_histogram(binwidth=0.05, fill="white", colour="#00754f") + theme_bw() +
  ggtitle("Distance of properties from a Starbucks") +
  scale_y_continuous(name="Total") +
  scale_x_continuous(name="Distance (km)", breaks=seq(0, 2.7, 0.1))
histogram

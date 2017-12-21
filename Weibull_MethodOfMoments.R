# Method of Moments for Weibull Distribution
library(zoo)

MyData <- read.csv(file="normalized_quantities.csv")

limitBuyMean <- MyData[1,2:11]
limitSellMean <- MyData[2,2:11]
cancelBuyMean <- MyData[3,2:11]
cancelSellMean <- MyData[4,2:11]

selectedOrder <- cancelSellMean # Change this line to select other orders.

densities <- c()
data <- c()

point <- 1

# Count data to empirical data
for(val in selectedOrder){
  densities <- c(densities, val)
  data <- c(data, rep(point, val))
  point <- point + 1
}

x = 1:10
mean = sum(x*densities) / sum(densities)
st_dev = sd(data)

shape = (st_dev/mean)^(-1.086)
scale = mean / gamma(1 + (1/shape))

# Location parameter is set to 1 since data starts from 1

wei_pmf <- function(shape, scale, x) {
  return((shape/scale) * (((x-1)/scale)^(shape-1)) * exp(-(((x-1)/scale)^shape)))
}

plot(1:10, densities/sum(densities), type="p",col="red", 
     xlab = "Distance from the best price (1 is the first tick)",
     ylab = "Probabilities", main = "Cancel Sell Orders (Weibull dist)")
lines(seq(1, 10, 0.01), wei_pmf(shape, scale, seq(1, 10, 0.01)), col="blue",
      ylim = max(wei_pmf(shape, scale, seq(1, 10, 0.01)))+0.1)

sum(wei_pmf(shape, scale, seq(1, 10, 0.01)))

legend("topright",
       c("Theoretical PMF","Empirical PMF"),
       fill=c("blue","red")
)

x <- seq(1,10,0.01)
y <- (shape/scale) * (((x-1)/scale)^(shape-1)) * exp(-(((x-1)/scale)^shape))
id <- order(x)

areaUnderCurve <- sum(diff(x[id])*rollmean(y[id],2))

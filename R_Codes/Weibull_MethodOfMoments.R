# Two Methods for Estimation of Weibull Distribution Parameters
library(zoo)

MyData <- read.csv(file="normalized_quantities.csv")

limitBuyMean <- MyData[1,2:11]
limitSellMean <- MyData[2,2:11]
cancelBuyMean <- MyData[3,2:11]
cancelSellMean <- MyData[4,2:11]

selectedOrder <- cancelBuyMean # Change this line to select other orders.

densities <- c()
data <- c()
data_v3 <- c()

# Start from 1
point <- 1

# Count data to empirical data
for(val in selectedOrder){
  densities <- c(densities, val)
  data <- c(data, rep(point, val))
  data_v3 <- c(data_v3, rep(point^3, val))
  point <- point + 1
}

# Start from 1
x = 1:10

# Mean and Standard Deviation
mean = sum(x*densities) / sum(densities)
st_dev = sd(data)

# Energy pattern factor method
epf = mean(data_v3) / (mean(data)^3)
shape = 1 + 3.69/(epf^2) 
scale = mean / gamma(1 + (1/shape))

# Empirical Method
shape = (st_dev/mean)^(-1.086)
scale = mean / gamma(1 + (1/shape))

# Location parameter is set to 1 since data starts from 1
wei_pmf <- function(shape, scale, x) {
  return((shape/scale) * (((x-1)/scale)^(shape-1)) * exp(-(((x-1)/scale)^shape)))
}

# Plot Empirical and Theoretical PMF
plot(1:10, densities/sum(densities), type="p",col="red", 
     xlab = "Distance from the best price (1 is the first tick)",
     ylab = "Probabilities", main = "Cancel Sell Orders (Weibull dist)")
lines(seq(1, 10, 0.01), wei_pmf(shape, scale, seq(1, 10, 0.01)), col="blue",
      ylim = max(wei_pmf(shape, scale, seq(1, 10, 0.01)))+0.1)

legend("topright",
       c("Theoretical PMF","Empirical PMF"),
       fill=c("blue","red")
)

# Area under the curve
x <- seq(1,10,0.01)
y <- (shape/scale) * (((x-1)/scale)^(shape-1)) * exp(-(((x-1)/scale)^shape))
id <- order(x)
areaUnderCurve <- sum(diff(x[id])*rollmean(y[id],2))
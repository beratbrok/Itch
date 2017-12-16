#install.packages('fitdistrplus')
library(fitdistrplus)

MyData <- read.csv(file="normalized_quantities.csv")

limitBuyMean <- MyData[1,2:11]
limitSellMean <- MyData[2,2:11]
cancelBuyMean <- MyData[3,2:11]
cancelSellMean <- MyData[4,2:11]

selectedOrder <- limitBuyMean # Change this line to select other orders.

data <- c()

# Choose this value as 1 for Weibull and Gamma, 0 for Exponential
i <- 0

# Count data to empirical data
for(val in selectedOrder) {
  data <- c(data, rep(i, val))
  i <- i+1
}

distExp <- fitdist(data, "exp", method = 'mle')
print(distExp)
gofstat(distExp)

distWeib <- fitdist(data, "weibull", method = 'mle')
print(distWeib)
gofstat(distWeib)

distGam <- fitdist(data, "gamma", method = 'mle')
print(distGam)
gofstat(distGam)


plot(distWeib)
plot(distGam)

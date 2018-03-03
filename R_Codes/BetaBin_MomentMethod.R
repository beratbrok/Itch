# Method of Moments for Beta Binomial Distribution

MyData <- read.csv(file="normalized_quantities.csv")

limitBuyMean <- MyData[1,2:11]
limitSellMean <- MyData[2,2:11]
cancelBuyMean <- MyData[3,2:11]
cancelSellMean <- MyData[4,2:11]

selectedOrder <- limitBuyMean # Change this line to select other orders.

densities <- c()

# Count data to empirical data
for(val in selectedOrder){
  densities <- c(densities, val)
}

# if densities has count data for zero data make start_val = 0
start_val = 1

# if densities has count data for zero data make n = length(densities)-1
n = length(densities)

x = start_val:n
m1 = sum(x*densities) / sum(densities)
m2 = sum(x^2*densities) / sum(densities)

a = (n*m1 - m2) / (n*(m2/m1 - m1 - 1) + m1)
b = ((n-m1)*(n-m2/m1))/(n*(m2/m1 - m1 - 1) + m1)

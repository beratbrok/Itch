# Two Methods for Estimation of Weibull Distribution Parameters
library(zoo)

MyData <- read.csv(file="nov_01_normalized_quantities.csv")

limitBuyMean <- MyData[1,2:11]
limitSellMean <- MyData[2,2:11]
cancelBuyMean <- MyData[3,2:11]
cancelSellMean <- MyData[4,2:11]

selectedOrder <- limitBuyMean # Change this line to select other orders.

obs <- c(1e-6, 1, 2, 3, 4, 5, 6, 7, 8, 9)
freq <- selectedOrder

data <- rep(obs, freq)

# Using Optim Function
# par[1] is shape
# par[2] is scale
logLik_wei <- function(x, par){
  -sum(log(par[1]) - par[1]*log(par[2]) + (par[1]-1) *log(x) - (x/par[2])^par[1])
}

optim(fn=logLik_wei, par = c(2,2), x = data)

# Using FitDistR Function
library("MASS")
fitdistr(data, "Weibull")


lst <- c(1,
         1,
         1.062961,
         1.099223,
         1,
         1.209125,
         1.031108,
         1,
         1.013034,
         1.028118,
         1.017719,
         1.001192,
         1.025716,
         1,
         1.057675,
         1,
         1,
         1.037506,
         1,
         1,
         1,
         1,
         1,
         1.115957,
         1,
         1,
         1.197397,
         1.039521)

mean(lst)
sd(lst) / sqrt(28)

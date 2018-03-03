# MLE for Beta Binomial Distribution

MyData <- read.csv(file="sep_20_normalized_quantities.csv")

limitBuyMean <- MyData[1,2:11]
limitSellMean <- MyData[2,2:11]
cancelBuyMean <- MyData[3,2:11]
cancelSellMean <- MyData[4,2:11]

selectedOrder <- cancelBuyMean # Change this line to select other orders.

obs <- c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
freq <- selectedOrder
data <- rep(obs, freq)

n = length(obs)-1

x = 0:n

# Using Optim Function
# par[1] is alpha
# par[2] is beta

loglik_bb <- function(x, n, par){
  -sum(log(choose(n, x)) + log(beta(x + par[1], n - x + par[2])) - log(beta(par[1], par[2])))
}

parameters = optim(fn=loglik_bb, par = c(1,1), x = data, n = n)$par

a = parameters[1]
b = parameters[2]

bb_pmf <- function(n, k, a, b) {
  return(choose(n,k)*beta(k+a, n-k+b)/beta(a,b))
}

# first plot
plot(0:9, freq/sum(freq),col="red", 
     xlab = "Distance from the best price (0 is the first tick)",
     ylab = "Probabilities", main = "Cancel Sell Orders (Beta Binomial dist)",
     pch=23, ylim=range(c(0,1)))

par(new = TRUE)
plot(0:9, bb_pmf(9,0:9,a,b), col="blue", pch=16, ylim=range(c(0,1)), axes = FALSE, xlab = "", ylab = "")
lines(0:9, bb_pmf(9,0:9,a,b), col="blue")

sum(bb_pmf(9,0:9,a,b))

legend("topright",
       c("Theoretical PMF","Empirical PMF"),
       fill=c("blue","red")
)

# Chi Squared Test for Beta Binomial

observed_freq <- as.numeric(selectedOrder)
expected_freq <- bb_pmf(9,0:9,a,b)*sum(selectedOrder)

chi_sq = sum((observed_freq - expected_freq)^2 / expected_freq)

# qchisq(0.95, degree of freedom)

# Limit Buy:    0.1054
# Limit Sell:   0.0613
# Cancel Buy:   0.1785
# Cancel Sell:  0.0840


pchisq(9, )

# CDF
# first plot
plot(0:9, cumsum(c(freq/sum(freq))),col="red", 
     xlab = "Distance from the best price (0 is the first tick)",
     ylab = "Probabilities", main = "Cancel Sell Orders (Beta Binomial dist)",
     pch=23, ylim=range(c(0,1)))

par(new = TRUE)
plot(0:9, cumsum(bb_pmf(9,0:9,a,b)), col="blue", pch=16, ylim=range(c(0,1)), axes = FALSE, xlab = "", ylab = "")
lines(0:9, cumsum(bb_pmf(9,0:9,a,b)), col="blue")


# Multinomial Sampling
# sample(y, 10, replace = TRUE)

# 4e 4 matris upper triangle
# hnull true olma olasiligi pvalue
# t test ile karsilastir 

# 20 deney sample al 4 grup icin de her deneyde 4 durum birbirleriyle t test en sonunda average al
# Conditional sor zehra hocaya
# 7 saatlik aralik icin beta binomial et, chisquared skoru cikar karsilastir pchisq() sonucu ile
# Kullback Leibler (KL)

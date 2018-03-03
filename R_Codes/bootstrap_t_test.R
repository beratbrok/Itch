# Bootstrap Sampling and T Test

MyData <- read.csv(file="normalized_quantities.csv")

limitBuyMean <- MyData[1,2:11]
limitSellMean <- MyData[2,2:11]
cancelBuyMean <- MyData[3,2:11]
cancelSellMean <- MyData[4,2:11]

orders <- c("Limit Buy Orders", "Limit Sell Orders", "Cancel Buy Orders", "Cancel Orders")
order_data <- list(limitBuyMean, limitSellMean, cancelBuyMean, cancelSellMean)

j <- 1

for (order in order_data) {
  
  cat("\n- ", orders[j], " -\n")
  j <- j + 1
  
  selectedOrder <- order # Change this line to select other orders.
  
  obs <- c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
  freq <- selectedOrder
  data <- rep(obs, freq)
  
  for (i in 1:20) {
    sampled_order <- sample(data, length(data), replace = TRUE)
    cat(i, "th sample - Mean: ", mean(sampled_order), ", St.Dev.: ", sd(sampled_order), "\n")
  }
  
  
}


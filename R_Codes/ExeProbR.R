library(plotly)

sep20_n_data <- read.csv(file="Quantities/sep_20_normalized_quantities.csv")
nov01_n_data <- read.csv(file="Quantities/nov_01_normalized_quantities.csv")
nov02_n_data <- read.csv(file="Quantities/nov_02_normalized_quantities.csv")
nov03_n_data <- read.csv(file="Quantities/nov_03_normalized_quantities.csv")

sep20_data <- read.csv(file="Quantities/sep_20_quantities.csv")
nov01_data <- read.csv(file="Quantities/nov_01_quantities.csv")
nov02_data <- read.csv(file="Quantities/nov_02_quantities.csv")
nov03_data <- read.csv(file="Quantities/nov_03_quantities.csv")

sep20_lim_buy <- sep20_data[1,2:10]
sep20_lim_sell <- sep20_data[2,2:10]
sep20_cancel_buy <- sep20_data[3,2:10]
sep20_cancel_sell <- sep20_data[4,2:10]
sep20_market_buy <- sep20_data[5,2:10]
sep20_market_sell <- sep20_data[6,2:10]

nov01_lim_buy <- nov01_data[1,2:10]
nov01_lim_sell <- nov01_data[2,2:10]
nov01_cancel_buy <- nov01_data[3,2:10]
nov01_cancel_sell <- nov01_data[4,2:10]
nov01_market_buy <- nov01_data[5,2:10]
nov01_market_sell <- nov01_data[6,2:10]

nov02_lim_buy <- nov02_data[1,2:10]
nov02_lim_sell <- nov02_data[2,2:10]
nov02_cancel_buy <- nov02_data[3,2:10]
nov02_cancel_sell <- nov02_data[4,2:10]
nov02_market_buy <- nov02_data[5,2:10]
nov02_market_sell <- nov02_data[6,2:10]

nov03_lim_buy <- nov03_data[1,2:10]
nov03_lim_sell <- nov03_data[2,2:10]
nov03_cancel_buy <- nov03_data[3,2:10]
nov03_cancel_sell <- nov03_data[4,2:10]
nov03_market_buy <- nov03_data[5,2:10]
nov03_market_sell <- nov03_data[6,2:10]

x <- c('09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18')
title_order <- c('September 20th', 'November 1st', 'November 2nd', 'November 3rd')

mls <- list()
mls[[1]] <- as.numeric(sep20_lim_buy)
mls[[2]] <- as.numeric(sep20_lim_sell)
mls[[3]] <- as.numeric(nov01_lim_buy)
mls[[4]] <- as.numeric(nov01_lim_sell)
mls[[5]] <- as.numeric(nov02_lim_buy)
mls[[6]] <- as.numeric(nov02_lim_sell)
mls[[7]] <- as.numeric(nov03_lim_buy)
mls[[8]] <- as.numeric(nov03_lim_sell)
j <- 1

for (i in seq(1, 7, 2)) {
  y1 <- as.numeric(mls[[i]])
  y2 <- as.numeric(mls[[i+1]])
  data <- data.frame(x, y1, y2)
  
  #The default order will be alphabetized unless specified as below:
  data$x <- factor(data$x, levels = data[["x"]])
  
  p <- plot_ly(data, x = ~x, y = ~y1, type = 'bar', name = 'Arrived Limit Buy Orders', marker = list(color = 'rgb(49,130,189)')) %>%
    add_trace(y = ~y2, name = 'Arrived Limit Sell Orders', marker = list(color = 'rgb(204,204,204)')) %>%
    layout(xaxis = list(title = "Hours", tickangle = -45),
           yaxis = list(title = "Quantities"),
           margin = list(b = 100),
           barmode = 'group',
           title = paste("Hourly Arrived Limit Orders on", title_order[j], sep = " "))
  p
  j <- j + 1
}

mls <- list()
mls[[1]] <- as.numeric(sep20_market_buy)
mls[[2]] <- as.numeric(sep20_market_sell)
mls[[3]] <- as.numeric(nov01_market_buy)
mls[[4]] <- as.numeric(nov01_market_sell)
mls[[5]] <- as.numeric(nov02_market_buy)
mls[[6]] <- as.numeric(nov02_market_sell)
mls[[7]] <- as.numeric(nov03_market_buy)
mls[[8]] <- as.numeric(nov03_market_sell)
j <- 1

for (i in seq(1, 7, 2)) {
  y1 <- as.numeric(mls[[i]])
  y2 <- as.numeric(mls[[i+1]])
  data <- data.frame(x, y1, y2)
  
  #The default order will be alphabetized unless specified as below:
  data$x <- factor(data$x, levels = data[["x"]])
  
  p <- plot_ly(data, x = ~x, y = ~y1, type = 'bar', name = 'Arrived Market Buy Orders', marker = list(color = 'rgb(49,130,189)')) %>%
    add_trace(y = ~y2, name = 'Arrived Market Sell Orders', marker = list(color = 'rgb(204,204,204)')) %>%
    layout(xaxis = list(title = "Hours", tickangle = -45),
           yaxis = list(title = "Quantities"),
           margin = list(b = 100),
           barmode = 'group',
           title = paste("Hourly Arrived Market Orders on", title_order[j], sep = " "))
  embed_notebook(p)
  j <- j + 1
}

mls <- list()
mls[[1]] <- as.numeric(sep20_cancel_buy)
mls[[2]] <- as.numeric(sep20_cancel_sell)
mls[[3]] <- as.numeric(nov01_cancel_buy)
mls[[4]] <- as.numeric(nov01_cancel_sell)
mls[[5]] <- as.numeric(nov02_cancel_buy)
mls[[6]] <- as.numeric(nov02_cancel_sell)
mls[[7]] <- as.numeric(nov03_cancel_buy)
mls[[8]] <- as.numeric(nov03_cancel_sell)
j <- 1

for (i in seq(1, 7, 2)) {
  y1 <- as.numeric(mls[[i]])
  y2 <- as.numeric(mls[[i+1]])
  data <- data.frame(x, y1, y2)
  
  #The default order will be alphabetized unless specified as below:
  data$x <- factor(data$x, levels = data[["x"]])
  
  p <- plot_ly(data, x = ~x, y = ~y1, type = 'bar', name = 'Arrived Cancel Buy Orders', marker = list(color = 'rgb(49,130,189)')) %>%
    add_trace(y = ~y2, name = 'Arrived Cancel Sell Orders', marker = list(color = 'rgb(204,204,204)')) %>%
    layout(xaxis = list(title = "Hours", tickangle = -45),
           yaxis = list(title = "Quantities"),
           margin = list(b = 100),
           barmode = 'group',
           title = paste("Hourly Arrived Cancel Orders on", title_order[j], sep = " "))
  embed_notebook(p)
  j <- j + 1
}










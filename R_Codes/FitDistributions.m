clear all;
clc;

filename = 'normalized_quantities.csv';
count_data = readtable(filename);

limit_buy_mean = table2array(count_data(1,2:11));
limit_sell_mean = table2array(count_data(2,2:11));
cancel_buy_mean = table2array(count_data(3,2:11));
cancel_sell_mean = table2array(count_data(4,2:11));

% Change this line to fit distributions to other data
selected_quantity = limit_buy_mean;

empirical_data = [];

for i=1:size(selected_quantity,2)
    for j=1:selected_quantity(i)
        empirical_data = [empirical_data; i];
    end
end

% Change second parameter to 'Exponential' or 'Gamma'
pd = fitdist(empirical_data,'Gamma')

x_values = 0:0.01:10;
y = pdf(pd,x_values);
plot(x_values,y,'LineWidth',2);
hold on;
scatter(1:10, selected_quantity/sum(selected_quantity));
xlabel('Distance From the Best Price')
ylabel('Quantity Density')
title('Gamma Distribution on Cancel Sell Orders')

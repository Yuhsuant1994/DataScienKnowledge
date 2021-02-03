# Regression

## Linear regression

[article goodness of fit, r-squared](https://blog.minitab.com/blog/adventures-in-statistics-2/regression-analysis-how-do-i-interpret-r-squared-and-assess-the-goodness-of-fit#:~:text=R%2Dsquared%20is%20a%20statistical,multiple%20determination%20for%20multiple%20regression.&text=100%25%20indicates%20that%20the%20model,response%20data%20around%20its%20mean.)

- calculate R2 to determine if X and Y are correlated.
- calculate a p-value to determine if R2 is statistically significant (null hypothesis that the coefficient is equal to zero which is no effect)

## Multiple regression, 

(need to check more)
same as linear regression, but use X, X1 to predict Y

### Compare linear / multiple

it can tell us do we need a more complex model to predict Y or we can just go with simple model


## Logistic regression (classification)

Try to predict 1/0, so the curve goes to 0 to 1. therefore after fitting linear regression to have the probability, 
it needs to fit into the sigmoid functions to have classifier to be 0 or 1. sigmoid fuction: <img src="https://miro.medium.com/max/674/0*pvMD0iSS8Mb2zy6W.png" width="100">

logistic regression doesn't have the same concept of residual as linear regression, so it cannot use least 
squares and it cannot calculate R2. instead it can use maximum likelihood (idea is to calculate the likelihood 
for all dots and multiply all of them together to get the likelihood of one line)

# Maximum likelihood VS R2 goodness of fit....

difference between linear regression and logistic regression


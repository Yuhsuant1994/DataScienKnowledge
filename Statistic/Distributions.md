# normal distribution

we can convert the data to standard normal distribution by this formula: 
Z = (X-µ) / σ, then 68.3% within 1 σ, (2: 95%, 3: 99.7%)

# poisson distribution

discrete probability distribution of number of events that occur in a specific 
period of time. useful for planning purpose (ex: analyze customer behavior 
as they visit the stroe)

(need to have a λ) the probability of 0 customer visiting the store can draw 
on curve. the probability of 7 or more customer visiting the store can draw 
another. we only have the average.

* events are independent.
* probability of event is proportional to time period 

P(x;µ) = (e^-µ^) (µ^X^) / x! (example if we only know average is 5 and we 
want to know p for 3 then we have the x = 3)

EX: a store sell 2 toys per day in average, what's the likelihood that 5 toys
will be sold tomorrow?

P(5;2) = (e^-2^)(2^5^)/5! = 0.036

# Binomial distirbution

measure the probability of success or failure outcome with experiments 
repeates several times. (N number of time, p success rate)

P(X) = (N!) / (x!(N-x)!) * pi^x^ * (1-pi)^N-x^

# Bernoulli distribution

sepecial case of binomial distribution where n = 1. single trial.

# reference recap

[video recap](https://www.youtube.com/watch?v=bmdsROmXgGI)
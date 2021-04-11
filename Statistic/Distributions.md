# probability distribution fuction

[youtube video](https://www.youtube.com/watch?v=YXLVjCKVP7U)

discrete: probability mass function (PMF)
continuous: probability density function (PDF)

to cumulative distribution function (CDF)

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

* 2 results
* events are independent.
* identical distribution (p the same)
* probability of event is proportional to time period 

P(x;µ) = (e^-µ^) (µ^X^) / x! (example if we only know average is 5 and we 
want to know p for 3 then we have the x = 3)

EX: a store sell 2 toys per day in average, what's the likelihood that 5 toys
will be sold tomorrow?

P(5;2) = (e^-2^)(2^5^)/5! = 0.036


# Binomial distirbution

measure the probability of success or failure outcome with experiments 
repeates several times. (N number of time, p success rate)

<img src="https://i.stack.imgur.com/MwwW6.png" height="300">

the distribution µ is the p for success, and std is `sqrt((P(1-P))/N)`

**Binomial example**
1. throw same dices for 50 times -> yes
2. draw 20 cards dont put back-> not identical card number is not infinity so the P is not the same in each draw
3. click on a search result page -> its not independant, people tend to click again when they don;t have the result they want
4. student finish course after 2 months -> yes (if the accounts meaning different person)
5. purchase item within  a week


## confidence interval
ph=X(sucess number)/N (total try)
Sanitory check if N*ph>5 and N*(1-ph)>5
confidence interval m (margin of error)
m=z*se
for Z(.95)=1



# Bernoulli distribution

sepecial case of binomial distribution where n = 1. single trial.

# reference recap

[video recap](https://www.youtube.com/watch?v=bmdsROmXgGI)



Dear DS & Analytics Community followers,

One month has past very fast, we are reaching our next meeting DS & Analytics Community 
which will take place on the 1st of April (Next Thursday) CEST 9:30 in Buchs/Schaan or 16:30 
in Kuala Lumpur/Singapore via the Microsoft Teams Link.

After an interesting Machine learning topic from Jonas being of this month, I will be the host and 
presenter this time. To talk about our projects in identifying unknow, unlinked contact to our 
database and create leads. We have a POC running in France using ElasticSearch Engine and we've 
received many request and interest in the projects from various market.

I will be presenting the brief of this project, how elasticsearch is set up and how does it work and
 some difficulties we are facing in designing the project and flow. 
Looking forward for the discussion.
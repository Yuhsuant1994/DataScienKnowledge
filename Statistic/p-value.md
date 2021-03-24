[from ref](https://support.minitab.com/en-us/minitab/18/help-and-how-to/statistics/basic-statistics/supporting-topics/basics/manually-calculate-a-p-value/?fbclid=IwAR1EO-lmsvo2rW0DYld280AXX8yiLhgslI_MGDSVC51s99TnSBw8xtU-OMc#:~:text=The%20p%2Dvalue%20is%20calculated,true)
* **cdf()**: Cumulative distribution function of the distribution of the test statistic (TS) under the null hypothesis
* **TS**: test statistic
* **P**: probablility of an event
* **ts**: observed value of the test statistic calulated from the sample

A p value for
* a lower-tailed test is specified by: p-value = P(TS  ts | H0 is true) = cdf(ts)
* an upper-tailed test is specified by: p-value = P(TS  ts | H0 is true) = 1 - cdf(ts)
* assuming that the distribution of the test statistic under H0 is symmetric about 0, a two-sided test is specified by: p-value = 2 * P(TS  |ts| | H0 is true) = 2 * (1 - cdf(|ts|))

P value (statistically significant test) is the probablility that the null hypothesis is true
so if the p value is small then it might reject the null hypothesis

A p-value less than 0.05 (typically ≤ 0.05) is statistically significant. 
It indicates strong evidence against the null hypothesis, as there is less 
than a 5% probability the null is correct (and the results are random). 
Therefore, we reject the null hypothesis, and accept the alternative hypothesis.
However, this does not mean that there is a 95% probability that the research 
hypothesis is true. The p-value is conditional upon the null hypothesis being 
true is unrelated to the truth or falsity of the research hypothesis.

[article, p-value](https://www.simplypsychology.org/p-value.html#:~:text=The%20smaller%20the%20p%2Dvalue,and%20the%20results%20are%20random)
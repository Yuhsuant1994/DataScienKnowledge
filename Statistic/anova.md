[one factor Anova](http://www.sthda.com/english/wiki/one-way-anova-test-in-r?fbclid=IwAR1pxwYmEwOIEMMvPlYOfAZpfszgqXYC7RbL_s9Xv5e1RrueHCe5kcgcBaY#summary)

[full ANOVA](https://statsandr.com/blog/anova-in-r/#post-hoc-test)

one-way analysis of variance (ANOVA): 
is a statistical test to determine whether two or more population means are different. 
In other words, it is used to compare two or more groups to see if they are significantly different.

Student t-test is used to compare 2 groups;
ANOVA generalizes the t-test beyond 2 groups, so it is used to compare 3 or more groups.

---------------

**Hypothesis**
* Null hypothesis: the means of the different groups are the same
* Alternative hypothesis: At least one group mean is not equal to the others.

we'll check the p-value to reject or not the null hypothesis

---------------------

**Test Assumptions**

1. Residuals should follow approximately a normal distribution

Can be test with **histogram** and **QQ plot**. And normality test **shapiro-Wilk** or **Kolmogorov-Smirnov**
[residual note](residuals.md)

(note that shapiro test null hypothesis is **Residual is normal distribution**)

2. Homogeneity of the variances:the variances of the different groups should be equal in the populations

This assumption can be tested **graphically** (by comparing the dispersion in a 
boxplot or dotplot for instance), or more formally via the **Levene’s test**
(leveneTest(variable ~ group) from the {car} package) or **Bartlett’s test**, 
among others. *If the hypothesis of equal variances is rejected*, another version 
of the ANOVA can be used: the Welch ANOVA (oneway.test(variable ~ group, var.equal = FALSE))

(note that Levene’s test null hypothesis is **variances are equal, homogeneity**)

3. **Independence** : the data, collected from a representative and randomly selected portion of the 
total population, should be independent between groups and within each group.

--------------------
**post-hoc tests**

After rejecting null hypothesis: (at least one group is different) which one? Multitesting problem, 
unlike slowly compare 2 group each time with t-test there could be some problem. let's see the 
equation, if significant level is `0.05` and we have `N` different group

```
P(at least one significant result) = 1 - P(no significant result)
                                   = 1 - (1 - 0.05)^N
```

the bigger the N is, the higher the probability is to reject null hypothesis, if `N=3` it's already 14.26%


The most often used are the **Tukey HSD** and **Dunnett’s tests**: (using residuals)
* **Tukey HSD** is used to compare **all groups** to each other (so all possible comparisons of 2 groups).
* **Dunnett** is used to make comparisons with a **reference group**. For example, consider 2 
treatment groups and one control group. If you only want to compare the 2 treatment groups with respect 
to the control group, and you do not want to compare the 2 treatment groups to each other, the 
Dunnett’s test is preferred.

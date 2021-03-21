*below info are the extract from multiple 
references sources, mainly serve as my own knowledge note*

Related side project analyzing A/B testing result: [Decrease Early Udacity Course Cancellation]()

# 1. A/B testing general

AB testing is the control expriment.

* Difference between **AB testing**, **split testing**

Split testing we can see it as a full different version, while A/B testing involved
in changing one elements. (a landing page / video / even things that user might not 
notice etc...)

We can also implement multivariate tests. but there are conditions,
1. the results are statistically significant
2. the population size must be large enough 

There often has some concerns:
* How to split control group and AB testing group
* The length of test period

Why do we need control group? control group would not see any variable changes,
on the other hand it can be seen as "do nothing". It is to alert **false positive**
exists within A/B testing. [(see my note for false positive explanation)][https://github.com/Yuhsuant1994/DataScienKnowledge/blob/master/DSConcept/recall_precision.md]

## 1.1, Some questions:

Should we use AB testing for all changes? AB testing can help you climb to the 
pick of this mountain but it cannot help you to choose whether you want to stay
in this mountain or go to another mountain.

what we shouldn't do with A/B testing? New experiments, people tend to react extrem 
interest or extrem reject in the first place might affect the result. However, we can 
still do with a good settings of baseline, and give some time buffer for user to get use
to the new experiment to see the more reliable result. (time is also tricky depending
on the nature of the site and business, people might not come frequently etc...)

Also AB testing cannot tell us if we are missing something. it can only be serve as a 
comparison. 

**bad example:**
1. is my site complete, this we cannot answer with AB testing, 
2. add premium service or not, we cannot fully answer too, assigning people to one
another wouldn't really work, we don't have control to compare against, but we can still gather info)
3. website selling cars / house: most A/B tests are run in a fairly short 
time window might be difficult to perform and compare

**good example:**
1. changing ranking algo: clear control variable, and metric
2. changing full backend: if we have capacity to run both version at the same time, yes.

## 1.2, Other technique than AB testing


-----------------------

# step by step note

## step 1: choose a matric
## step 2: review statistic
## step 3: design experiment
## step 4: analyze result



# reference
* [UDACITY free AB testing course](https://www.udacity.com/course/ab-testing--ud257)
    this course focus more about the 
* [How to do A/B Testing](https://www.crazyegg.com/blog/ab-testing/)
* [what is control group](https://clevertap.com/blog/what-is-a-control-group/)
* [AB testing projects](https://github.com/baumanab/udacity_ABTesting#summary)
* [AB testing good notebook](https://www.kaggle.com/tammyrotem/ab-tests-with-python/notebook)
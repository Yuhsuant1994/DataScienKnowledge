# Bag of words
[EXAMPLE](bow_simple_example.py)

To start BOW we define the vocabulary we want to learn

|vocabulary|
|---|
|dataframe|
|colors|
|columns|
|plot|
|graph|

then we need to define some label to the topic
|possible labels|
|---|
|pandas|
|keras|
|matplotlib|

input: how to **plot** **dataframe** bar **graph**
-> [1 0 0 1 0 1 0 0 0 0]  (nothing to do with the orders)

prediction: **pandas** keras **matplotlib** -> [1 0 1]

inputs to prediction: after it become an array we can simpily do calculations inputs*weights+bias


## BOW to apply

Step 1: preprocessing (lower, stemming/lemminization, stop words)

Step 2: we create a histogram of the frequency to place in decending orders

Step 3: creating a vector from the frequency (here BOW will be how many time the word is presenting
but in the binary BOW is the only 1,0 if it shown in the sentence or not) then those word will become
the independent feature of BOW.

## Disadvantage BOW

every word has the same weight, no feature (word) is more important. TFIDF is mainly to solve this disadvantage,
if we have huge data set this is going to be slow, we should use word2vec instead.

#TF-IDF

* Term Frequency (TF): $1/2$ $a/bdsfojdf$ $1/2$ $a/{alkjvoer}$

$1/2$ $a/bdsfojdf$

$1/2$ $a/{alkjvoer}$
<img src="https://render.githubusercontent.com/render/math?math=a/{alkjvoer}">
```math
1/2 
a/bdsfojdf
a/{bdsfojdf}

```

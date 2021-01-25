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

# TF-IDF

![!image](https://www.quentinfily.fr/wp-content/uploads/2015/11/td-idf-graphic.png | width=500)

## Term Frequency (TF):{# of target of words in sentence}/{# of words in sentence}

we can think of how important is this word in this sentence

```
s1: good boy    s2: good girl    s3: boy girl good
```
|  |s1|s2|s3|
|--|--|--|--|
|good|1/2|1/2|1/3|
|boy|1/2|0|1/3|
|girl|0|1/2|1/3|

## inverse document frequency (IDF) log({# of sentence}/{# of sentence contain target words})
![!image](https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Logarithme_neperien.svg/1200px-Logarithme_neperien.svg.png)


<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Logarithme_neperien.svg/1200px-Logarithme_neperien.svg.png" width="500">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Logarithme_neperien.svg/1200px-Logarithme_neperien.svg.png" hight="100">


<img src="https://www.quentinfily.fr/wp-content/uploads/2015/11/td-idf-graphic.png" width="500">
<img src="https://www.quentinfily.fr/wp-content/uploads/2015/11/td-idf-graphic.png" hight="100">


![!image](https://www.quentinfily.fr/wp-content/uploads/2015/11/td-idf-graphic.png | width=500)


we can think as more sentence contain the word, less important the word is
|words|IDF|
|==|==|
|good|ln(3/3)=0|
|boy|ln(3/2)|
|git|ln(3/2)|



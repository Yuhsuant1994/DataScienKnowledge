[NLP EXAMPLE](nlp_simple_example.py)

[Youtube review channel](https://www.youtube.com/playlist?list=PLZoTAELRMXVMdJ5sqbCK2LiM0HhQVWNzm)


# Bag of words

```
s1: good boy    s2: good girl    s3: boy girl good
```
|  |good|boy|girl|
|--|--|--|--|
|s1|1|1|0|
|s2|1|0|1|
|s3|1|1|1|

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

to fix the disadvantage of BOW

<img src="https://www.quentinfily.fr/wp-content/uploads/2015/11/td-idf-graphic.png" width="500">

* Term Frequency (TF):
`num of target of words in sentence/number of words in sentence`

we can think of how important is this word in this sentence

```
s1: good boy    s2: good girl    s3: boy girl good
```
|  |s1|s2|s3|
|--|--|--|--|
|good|1/2|1/2|1/3|
|boy|1/2|0|1/3|
|girl|0|1/2|1/3|

* inverse document frequency (IDF) 

`log(number of sentence/ number of sentence contain target words)`

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Logarithme_neperien.svg/1200px-Logarithme_neperien.svg.png" width="300">

we can think as more sentence contain the word, less important the word is

|words|IDF|
|--|--|
|good|ln(3/3)=0|
|boy|ln(3/2)|
|git|ln(3/2)|

* final vector (need to reverse)

here we can see in s1 boy is more important than good, since good is in every sentences so it is not important.
 Then we use f1-f3 dependent feature to train output independant feature

| |f1 <br> good|f2 <br> boy|f3 <br> girl|output <br> feature|
|--|--|--|--|--|
|s1|0|1/2 * log(3/2)|0||
|s2|0|0|1/2 * log(3/2)||
|s3|0|1/3 * log(3/2)|1/3 * log(3/2)||

# Word2vec

to solve the above 2 method since words has no semantic informaiton (relation in meaning between words), as King-Man+Woman=Queen.
 those this can lead to over fitting

each word is represented as a vector of 32 or more dimension instead of a single number




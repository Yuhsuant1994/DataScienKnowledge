#Nature Process Languages
In DS we tend to turn our data into matrices or tensors, like in image processing, 
however in NLP we need to turn words into numbers so we can stick them into the matrices

## Important step to do before starting
[example](preprocess.py)

### Tokenization
`Tokenization Library to use often: nltk`
converting paragraph to sentences list or to word list. 

###stemming and lemmatization
process of reducing infected words to their word stem. Stemming is generally enough if today 
we are just seeing a post is possitive or negative, the stem part of the word generally is enough;
whereas lemmatization is going to convert to meaningful words. in chatbot we need lemmatization, 
because the response needs to be meaningful.

Stemming Examples:
problem produce intermediate representation of the word may not have any meaning, but we have less words
```
[history, historical] -> histori
[finally, final, finalized]->fina
[going, goes, gone] -> go
```
lemmatization example:
```
[history, historical] -> history
[finally, final, finalized]->final
[going, goes, gone] -> go
```

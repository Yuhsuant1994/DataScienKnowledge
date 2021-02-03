import nltk
#nltk.download()

paragraph="""
Natural language processing (NLP) is a subfield of linguistics, computer science, 
artificial intelligence concerned with the interactions between computers and human 
language, in particular how to program computers to process and analyze large amounts 
of natural language data. The result is a computer capable of "understanding" the contents 
of documents, including the contextual nuances of the language within them. The technology 
can then accurately extract information and insights contained in the documents as well as 
categorize and organize the documents themselves.
"""
sentences=(nltk.sent_tokenize(paragraph))

#even the punctuation is consider as a words
words=(nltk.word_tokenize(paragraph))

#stemming
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

#stopwords.words('english') #->we can see a big list of stop words in english

sentences=(nltk.sent_tokenize(paragraph))
stemmer=PorterStemmer()
lemmatizer=WordNetLemmatizer()

#for every sentences we remove stopwords
for i in range(len(sentences)): #how many sentences
    words=nltk.word_tokenize(sentences[i])
    #words=[stemmer.stem(word) for word in words if word not in set(stopwords.words('english'))]
    words=[lemmatizer.lemmatize(word) for word in words if word not in set(stopwords.words('english'))]
    #set help to take only the unique set of words
    sentences[i]=' '.join(words)
    print(sentences[i])


#print(words)
print('hi')
import nltk
#clean text 
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import unicodedata
#bow
from sklearn.feature_extraction.text import CountVectorizer

#word2vec
from gensim.models import Word2Vec

def strip_accents(text):
   try:
       text = unicode(text, 'utf-8')
   except (TypeError, NameError): # unicode is a default on python 3 
       pass
   text = unicodedata.normalize('NFD', text)
   text = text.encode('ascii', 'ignore')
   text = text.decode("utf-8")
   return str(text)

paragraph = """I have three visions for India. In 3000 years of our history, people from all over 
               the world have come and invaded us, captured our lands, conquered our minds. 
               From Alexander onwards, the Greeks, the Turks, the Moguls, the Portuguese, the British,
               the French, the Dutch, all of them came and looted us, took over what was ours. 
               Yet we have not done this to any other nation. We have not conquered anyone. 
               We have not grabbed their land, their culture, 
               their history and tried to enforce our way of life on them. 
               Why? Because we respect the freedom of others.That is why my 
               first vision is that of freedom. I believe that India got its first vision of 
               this in 1857, when we started the War of Independence. It is this freedom that
               we must protect and nurture and build on. If we are not free, no one will respect us.
               My second vision for India’s development. For fifty years we have been a developing nation.
               It is time we see ourselves as a developed nation. We are among the top 5 nations of the world
               in terms of GDP. We have a 10 percent growth rate in most areas. Our poverty levels are falling.
               Our achievements are being globally recognised today. Yet we lack the self-confidence to
               see ourselves as a developed nation, self-reliant and self-assured. Isn’t this incorrect?
               I have a third vision. India must stand up to the world. Because I believe that unless India 
               stands up to the world, no one will respect us. Only strength respects strength. We must be 
               strong not only as a military power but also as an economic power. Both must go hand-in-hand. 
               My good fortune was to have worked with three great minds. Dr. Vikram Sarabhai of the Dept. of 
               space, Professor Satish Dhawan, who succeeded him and Dr. Brahm Prakash, father of nuclear material.
               I was lucky to have worked with all three of them closely and consider this the great opportunity of my life. 
               I see four milestones in my career"""

"""
step 1 : preprocessing the text
"""
# Preprocessing the data
text = re.sub(r'\[[0-9]*\]',' ',strip_accents(paragraph))# remove number special character
#text=re.sub('[^a-zA-Z]', ' ', text) # if we remove puncatuation there's no sentences. it should be remove in the sentences
text = re.sub(r'\s+',' ',text)
text = text.lower()
text = re.sub(r'\d',' ',text)
text = re.sub(r'\s+',' ',text) #remove extra space

##usually lemmatization take more time to make sure the words have meaning
stemmer=PorterStemmer()
wordnet=WordNetLemmatizer()
sentences = nltk.sent_tokenize(text) #this is for tf-idf, bow
sentences_w2v=nltk.sent_tokenize(text) #this format is for word2vec

for i in range(len(sentences)):
   words=nltk.word_tokenize(re.sub('[^a-zA-Z]', ' ', sentences[i]))
   sentences_w2v[i]=[stemmer.stem(word) for word in words if word not in set(stopwords.words('english'))] ##with no meaning
   #words=[lemmatizer.lemmatize(word) for word in words if word not in set(stopwords.words('english'))]
   sentences[i]=' '.join(sentences_w2v[i])
"""
BOW
"""
cv = CountVectorizer(max_features=1500)
X = cv.fit_transform(sentences).toarray()
#this library contain BOW

"""
TF-ITF
"""

from sklearn.feature_extraction.text import TfidfVectorizer
cv = TfidfVectorizer()
X = cv.fit_transform(sentences).toarray()


"""
Word2Vec
"""      
# Training the Word2Vec model
model = Word2Vec(sentences_w2v, min_count=1)
##generally take 2 ignore if count(word)<=2, 
##but here we have small data set so we take 1

words = model.wv.vocab
#find outall the vocabulary that was collected every work we get a vector of 100 dimension


# Finding Word Vectors
vector = model.wv['war']
#to see the vector of that word

# Most similar words
similar = model.wv.most_similar('artificial')
# get the words that is similar word to it

print('hi')


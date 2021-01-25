import nltk

paragraph="""
Natural language processing (NLP) is a subfield of linguistics, computer science, 
artificial intelligence concerned with the interactions between computers and human 
language, in particular how to program computers to process and analyze large amounts 
of natural language data. The result is a computer capable of "understanding" the contents 
of documents, including the contextual nuances of the language within them. The technology 
can then accurately extract information and insights contained in the documents as well as 
categorize and organize the documents themselves.
"""



#clean text 
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

ps=PorterStemmer()
wordnet=WordNetLemmatizer()
sentences=(nltk.sent_tokenize(paragraph))
#//stemmer//
import nltk
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
def stemmer_words(words):
    list_words=[]
    for word in words:
        list_words=stemmer.stem(words)
        list_words.append(list_words)

    return list_words
#//lemmatizer//
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
def lem_verbs(words):
    lem_verbs=[]
    for word in words:
        lem_verbs=lemmatizer.lemmatize(word,'v')
        lem_verbs.append(lem_verbs)
    return lem_verbs

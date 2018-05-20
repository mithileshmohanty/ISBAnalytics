
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re

def textCharacterstics(text):
    print("Total Number of Characters: %s" %len(text))
    listOfWords=text.split(' ')
    print("Total Number of Texts: %s" %len(listOfWords))
    print("Avg Number of Characters per word: %s" %(len(text)/len(listOfWords)))

def cleanTextBlock(text,stopWords=None,removeStopWords=True,removeNumbers=True,lengthFilterLimit=2):
    text=text.lower()
    text=re.sub(r'<.*?>','',text)
    text=re.sub(r'[^\w\s]','',text)
    if removeNumbers:
        text=re.sub(r'[0-9]','',text)
    if removeStopWords:
        stopWords = stopwords.words('english')
    listTokenized=text.split(" ")
    #print(len(listTokenized))
    listLemmantized=[]
    for word in listTokenized:
        if word and len(word) >lengthFilterLimit and not re.match(r'^http',word) and not re.match(r'^www',word) and ((removeStopWords and word not in stopWords) or not removeStopWords):
                lemmentizer=WordNetLemmatizer()
                listLemmantized.append(lemmentizer.lemmatize(word))
    #print(len(listLemmantized))
    return listLemmantized
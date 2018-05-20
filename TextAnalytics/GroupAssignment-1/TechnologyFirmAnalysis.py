import subprocess
import feather
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
from gensim import corpora
from gensim.models import TfidfModel
import os
import gensim
import numpy
import matplotlib.pyplot as plt
from wordcloud import WordCloud

plt.rcdefaults()

def generateDTMDifference(dataFrameOld,newDataFrame,path=None):
    listOfNew=list(set(newDataFrame["Word"]) - set(dataFrameOld["Word"]))
    df=newDataFrame[newDataFrame['Word'].isin(listOfNew)]
    dataBox=df.groupby(['Frequencies']).size().reset_index(name='Counts')
    df.loc[:,['Word','Frequencies']].sort_values('Frequencies', ascending=False).to_csv(path+".tsv", sep='\t')
    if path:
        title="Frequency of Occurences of new Words per Word for %s" %path[-8:]
    else:
        title=""
    showBoxPlot(dataBox['Counts'].tolist(),dataBox['Frequencies'].tolist(),title,'No Of Words','Frequencies of individual Words',path,True)
    stringText=""
    #print(df)
    dictWord=pd.Series(df.Frequencies.values,index=df.Word).to_dict()
    #print(dictWord)
    for key,value in dictWord.items():
        for i in range(0,value):
            stringText+=" "+key
    #print(stringText)
    if path:
        title="Word Cloud for %s" %path[-8:]
    else:
        title=""
    showWordCloud(stringText,title,path,True)
    return df


def showWordCloud(data, title = None, path=None,show=False):
    wordcloud = WordCloud(background_color='black',stopwords=stopWords,max_words=200,max_font_size=40,scale=3,random_state=1,width=600,height=600).generate(str(data))
    plt.axis('off')
    if title: 
        plt.title(title)
    plt.imshow(wordcloud)
    if path:
        plt.savefig(path+'_WordCloud.png',bbox_inches='tight',dpi=300)  
    if show:
        plt.show()
    plt.close()
    
    
def showBoxPlot(xData,yData,title=None,xLabel=None,yLable=None, path=None,show=False):
    yItems =xData
    xItems = yData
    y_pos = numpy.arange(len(xItems))
    plt.bar(y_pos, yItems)
    if yLable:
        plt.ylabel(yLable)
    if xLabel:
        plt.ylabel(xLabel)
    if title: 
        plt.title(title)
    plt.xticks(y_pos, xItems)
    if path:
        plt.savefig(path+'_BarPlot.png',bbox_inches='tight',dpi=300)
    if show:
        plt.show()
    plt.close()

def textCharacterstics(text):
    print("Total Number of Characters: %s" %len(text))
    listOfWords=text.split(' ')
    print("Total Number of Texts: %s" %len(listOfWords))
    print("Avg Number of Characters per word: %s" %(len(text)/len(listOfWords)))

def cleanTextBlock(text,stopWords,removeStopWords=True,removeNumbers=True,lengthFilterLimit=2):
    text=text.lower()
    text=re.sub(r'<.*?>','',text)
    text=re.sub(r'[^\w\s]','',text)
    if removeNumbers:
        text=re.sub(r'[0-9]','',text)
    listTokenized=text.split(" ")
    #print(len(listTokenized))
    listLemmantized=[]
    for word in listTokenized:
        if word and len(word) >lengthFilterLimit and not re.match(r'^http',word) and not re.match(r'^www',word) and ((removeStopWords and word not in stopWords) or not removeStopWords):
                lemmentizer=WordNetLemmatizer()
                listLemmantized.append(lemmentizer.lemmatize(word))
    #print(len(listLemmantized))
    return listLemmantized

def createDTM(corporaList,path):
    dictionary = corpora.Dictionary(corporaList)
    #dictionary.save(path+'.dict')
    corpus = [dictionary.doc2bow(text) for text in corporaList]
    #corpora.MmCorpus.serialize(path+'.mm', corpus)
    ndArray=gensim.matutils.corpus2dense(corpus, len(dictionary))
    numpy.savetxt(path+".csv", ndArray, delimiter=",")
    items=[]
    for i in range(0,len(dictionary)):
        items.append([i,dictionary[i],dictionary.dfs[i]])
    dataFrame = pd.DataFrame(items,columns=['Id','Word','Frequencies'])
    dataFrame.sort_values('Frequencies', ascending=False).to_csv(path+".tsv", sep='\t')
    df=dataFrame.groupby(['Frequencies']).size().reset_index(name='Counts')
    showBoxPlot(df['Counts'].tolist(),df['Frequencies'].tolist(),"Frequency of Occurences per Word for %s" %path[-4:],'No Of Words','Frequencies of individual Words',path)
    stringText=""
    for sublist in corporaList:
        stringText+=" ".join(sublist)
    showWordCloud(stringText,"Word Cloud for %s" %path[-4:],path)
    model = TfidfModel(corpus) 
    corpus_tfidf = model[corpus]  
    #corpora.MmCorpus.serialize(path+'_tfidf.mm', corpus_tfidf)
    ndArray=gensim.matutils.corpus2dense(corpus_tfidf, len(dictionary),dtype=numpy.int16)
    numpy.savetxt(path+"_tfidf.csv", ndArray, delimiter=",")


if not os.path.exists(".\\Output"):
    os.makedirs(".\\Output")
stopWords = stopwords.words('english')
subprocess.check_call(['Rscript', 'ConvertRdsToFeather.R'], shell=False)    
documentDictionary={}

for year in range(2005,2015):
    corporaList=[]
    for index,row in feather.read_dataframe(str(year)+".feather").iterrows():
        #textCharacterstics(row["bd.text"])
        corporaList.append(cleanTextBlock(row["bd.text"],stopWords))
    os.remove(str(year)+".feather")
    print("Creating DTM for Year: %s" %year)
    createDTM(corporaList,'.\\Output\\'+str(year))
    corporaList.clear()
    print("completed DTM for Year: %s" %year)

df_dict = pd.read_csv('.\\Output\\2005.tsv', sep='\t')

for year in range(2006,2015):
    df_new = pd.read_csv('.\\Output\\'+str(year)+'.tsv', sep='\t')
    df=generateDTMDifference(df_dict,df_new,'.\\Output\\'+str(year)+"_New")
    print(len(df_dict))
    print(len(df_new))
    df_dict=df_dict.append(df)
    print(len(df_dict))


    
    



    



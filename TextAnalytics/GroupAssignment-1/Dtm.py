from wordcloud import WordCloud
from gensim import corpora
from gensim.models import TfidfModel
import gensim
import numpy
import pandas as pd
from PlotGraph import showBoxPlot
from PlotGraph import showWordCloud

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
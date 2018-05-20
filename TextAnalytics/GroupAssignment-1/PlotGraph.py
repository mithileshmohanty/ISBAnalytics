import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
import numpy
plt.rcdefaults()

def showWordCloud(data, title = None, path=None,show=False):
    stopWords = stopwords.words('english')
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
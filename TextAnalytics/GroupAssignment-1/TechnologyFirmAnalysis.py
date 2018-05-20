import subprocess
import feather
import pandas as pd
import os
from urllib.request import urlopen

data = urlopen("https://cdn.rawgit.com/mithileshmohanty/ISBAnalytics/174aa8c0/TextAnalytics/GroupAssignment-1/CleanText.py")
f=open('CleanText.py', "w") 
t="".join(map(chr, data.read()))
f.write(t)
f.close()
data = urlopen("https://cdn.rawgit.com/mithileshmohanty/ISBAnalytics/174aa8c0/TextAnalytics/GroupAssignment-1/PlotGraph.py")
f=open('PlotGraph.py', "w") 
t="".join(map(chr, data.read()))
f.write(t)
f.close()
data = urlopen("https://cdn.rawgit.com/mithileshmohanty/ISBAnalytics/174aa8c0/TextAnalytics/GroupAssignment-1/Dtm.py")
f=open('Dtm.py', "w") 
t="".join(map(chr, data.read()))
f.write(t)
f.close()

ct = __import__("CleanText")
d = __import__("Dtm")

if not os.path.exists(".\\Output"):
    os.makedirs(".\\Output")
subprocess.check_call(['Rscript', 'ConvertRdsToFeather.R'], shell=False)    
documentDictionary={}

for year in range(2005,2015):
    corporaList=[]
    for index,row in feather.read_dataframe(".\\Temp\\"+str(year)+".feather").iterrows():
        #ct.textCharacterstics(row["bd.text"])
        corporaList.append(ct.cleanTextBlock(row["bd.text"]))
    os.remove(".\\Temp\\"+str(year)+".feather")
    print("Creating DTM for Year: %s" %year)
    d.createDTM(corporaList,'.\\Output\\'+str(year))
    corporaList.clear()
    print("completed DTM for Year: %s" %year)

df_dict = pd.read_csv('.\\Output\\2005.tsv', sep='\t')

for year in range(2006,2015):
    df_new = pd.read_csv('.\\Output\\'+str(year)+'.tsv', sep='\t')
    df=d.generateDTMDifference(df_dict,df_new,'.\\Output\\'+str(year)+"_New")
    print(len(df_dict))
    print(len(df_new))
    df_dict=df_dict.append(df)
    print(len(df_dict))



    
    



    



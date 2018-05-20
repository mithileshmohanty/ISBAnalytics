import subprocess
import feather
import pandas as pd
import os
from CleanText import cleanTextBlock
from CleanText import textCharacterstics
from Dtm import createDTM
from Dtm import generateDTMDifference

if not os.path.exists(".\\Output"):
    os.makedirs(".\\Output")
subprocess.check_call(['Rscript', 'ConvertRdsToFeather.R'], shell=False)    
documentDictionary={}

for year in range(2005,2015):
    corporaList=[]
    for index,row in feather.read_dataframe(".\\Temp\\"+str(year)+".feather").iterrows():
        #textCharacterstics(row["bd.text"])
        corporaList.append(cleanTextBlock(row["bd.text"]))
    os.remove(".\\Temp\\"+str(year)+".feather")
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



    
    



    



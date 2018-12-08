from urllib.request import urlopen
data = urlopen("https://cdn.jsdelivr.net/gh/mithileshmohanty/ISBAnalytics/TextAnalytics/GroupAssignment-1/TechnologyFirmAnalysis.py")
#print(data.read())
f=open('test1.py', "w") 
t="".join(map(chr, data.read()))
print(t)
f.write(t)
f.close()
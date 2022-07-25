import pandas as pd
import nltk

with open('words/palavras.txt', 'r', encoding="utf-8") as file:
    palavras = file.read().splitlines()

palavras.extend(['bolsonaro','ciro','gomes','17','13','pt','psdb','psol','pcdob','pl','psb','pdt','anitta'])

ats = pd.read_csv('../../Data/TikTokUsers.csv')
ats = ats['Url'].to_list()
ats = [x.split('m/')[1] for x in ats]

stopwords = nltk.corpus.stopwords.words('portuguese')

palavras.extend(ats)
newwords = [x.lower() for x in nltk.corpus.mac_morpho.words()]
palavras.extend(newwords)
newwords = [x.lower() for x in nltk.corpus.machado.words()]
palavras.extend(newwords)
#palavras.extend(words.words()) (english words)
palavras = [x for x in palavras if len(x) > 1]

palavras = set(palavras)

#remove stopwords
for i in stopwords:
    if i in palavras:
        palavras.remove(i)

with open('words/corpus.txt','w',encoding="utf-8") as file:
    for palavra in palavras:
        file.write(palavra.lower()+'\n')


import calendar
import requests
import datetime as dt
import json

import numpy
import pandas
import codecs
import pickle



#def CategoryCapture(lang, category):
path = '/Users/awwad/Downloads/Bayesian space/'

def CategoryCapture(lang, categ):
    print "HIHO"
    category=categ
    kat = 'Category:'
    #url = 'https://'+lang+'.wikipedia.org/w/api.php?action=query&format=json&cmtitle='+category+'&list=categorymembers&cmlimit=500&format=json'
    url='https://'+lang+'.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle='+category+'&cmlimit=500&format=json'
    
    r = requests.get(url)
    #print r.json()['query']['categorymembers']
    cats = r.json()['query']['categorymembers']
    print "len cats=",len(cats)
    
    if len(cats)==500:
        while 'continue' in r.json():
            r = requests.get(url+'&cmcontinue='+r.json()['continue']['cmcontinue'])
            cats = cats+r.json()['query']['categorymembers']
    di={}
    
    print "&*&*&*&*&*&**&*&*&*&*&*&*&*&*&*&*&*&*&*&&*&*&*&*&*&*&*&*&*&*"
    kats=[]
    count=len(cats)
    if category not in di:
        di[category]=[]
    print "Len cats",len(cats)
    for cat in cats:
        if kat not in cat['title'] and 'Portal:' not in cat['title']: #If title contains no 'Category:' prefix
            #print "B",cat['title']
            print "PTY1:",type(cat['title']),cat['title']
            di[category].append(cat['title'])
        elif 'Portal:' not in cat['title'] :
            print "PTY2:",type(cat['title']),cat['title']
            kats.append(cat['title'])  
    kk=1
    while True:
        print "kk=",kk,
        kk=kk+1
        if len(kats)<1:
            break
        else:
            category=kats.pop(0)
            url='https://'+lang+'.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle='+category+'&cmlimit=500&format=json'
            
            r = requests.get(url)
            print url
            cats = r.json()['query']['categorymembers']
            
            if len(cats)==500:
                while 'continue' in r.json():
                    r = requests.get(url+'&cmcontinue='+r.json()['continue']['cmcontinue'])
                    cats = cats+r.json()['query']['categorymembers']
            if category not in di:
                di[category]=[]
            for cat in cats:
                if kat not in cat['title'] and 'Portal:' not in cat['title']: #If title contains no 'Category:' prefix
                    #print "B",cat['title']
                    di[category].append(cat['title'])
                elif 'Portal:' not in cat['title']:
                    kats.append(cat['title'])  
            #di[category]=cats #there's your mistake
            #print "LEN",len(cats),category, di[category],"|||"
        count=count+len(cats)
    
    #if di[category]=0 recursion ends, but maybe there's error of no categorymembers
    
    
    print len(kats)
    print "COUNT:",count
    #print kats
    print "+++++++++++++++++++++++++++++++++"
    print len(di[category])

    return di

def CategoryLinks(lang,categ, lev):
    CC=CategoryCapture(lang,categ)
    articles=[]
    print 'LLX',type(articles)
    print articles
    for c in CC:
        print '**',c,CC[c][0]
        for k in CC[c]:
            print "++",k,
            articles.append(k['title'])
    print 'LLo',len(articles)

    if lev<=0:
        print "HIHIHI"
        return set(articles)
    print "PP",articles
    arts = set(list(articles))
    all_arts = arts
    
    print "########################################################## For 0:",len(arts)
    for i in range(lev):
        print "*********************************************************************************************************************"
        arts2=set()
        for a in arts:
            print "("+a+")",
            arts2=arts2|set(linkripTitles('https://'+lang+'.wikipedia.org/wiki/'+a).keys())
        all_arts = all_arts|arts2
        arts=arts2
        print "\n########################################################## For "+str(i+1)+":",len(arts2)   
    return set(all_arts)

def CatCapFlat(lang,categ):
    CC=CategoryCapture(lang,categ)
    articles=[]
    print 'LL',type(articles)
    for c in CC:
        articles=articles+(CC[c])
    print 'LL',type(articles)

    #if lev<=0:
    #    print "HIHIHI"
    #    return set(articles)
    print "//////////////*****",articles,"*****////////////"
    print "LIST LENGTH",len(articles)
    arts = set(list(articles))
    all_arts = arts
    DD={}
    c=1
    print "Looping",len(arts),"values"
    for a in arts:
        print "#"+str(c),
        DD[a]=set(linkripTitles('https://'+lang+'.wikipedia.org/wiki/'+a).keys())
        c=c+1
    
    return DD        


#-MAIN

lang = 'en'
#category=["" for _ in range(3)]
category= ['Category:Statistical_analysis','Category:Econometrics','Category:Machine_learning']
category= ['Category:History of Munich','Category:Economy of Munich']

print "L",len(category)

blist2=[]
blist=[]
flist=[]
keyz=[]

bdic={}
lus=[dict(),dict(),dict()]
blat=set()

for i in range(0,1): #!!! shud b 3
        
    pkl_file = open(path+category[i][category[i].index(':')+1:]+'2.p', 'rb')
    data1 = pickle.load(pkl_file)
    bdic.update(data1)
    print len(data1), type(data1)
    
    lus[i]=bdic.keys()
    keyz=keyz+lus[i]
    
    flat=set()
    flist=[]
    for d in data1:
        if len(data1[d])>40:
            print d+":",len(data1[d]),"<>",
        #print "XY",len(flat), type(data1[d])
        flat=flat|set([d])
        flat=flat|set(data1[d])
        flist=flist+[d]
        flist=flist+list(data1[d])
        #print len(flat),
    blat=blat|flat
    print "Count:",len(flat),"fLIST:",len(flist), len(set(flist))
    blist = blist+flist
    print "LEN BLAT",len(blat)
print "..............................................."
lenk = len(keyz)
print "LK1", len(keyz)

blat = list(blat)
blat.sort()

for k in range(0, lenk):
    j=keyz[lenk-1-k]
    for _ in [':_',': ',' :','_:']:
        j=j.replace(_,'')
    if ':' in j or '(page does not exist)' in j:
        print "Bad!",keyz[lenk-1-k],
        del keyz[lenk-1-k]
lenb=len(blat)
print "\n\n\nPASS 1\n\n\n"

for k in range(0, lenb):
    j=blat[lenb-1-k]
    for _ in [':_',': ',' :','_:']:
        j=j.replace(_,'')
    if ':' in j or '(page does not exist)' in j:
        print "Bad!",blat[lenb-1-k],
        del blat[lenb-1-k]


print "\nLK2", len(keyz)
print "LEN blat now", len(blat)
print "LD",len(bdic)
print "BLI:",len(blist2),len(set(blist2))
print "BLI:",len(blist),len(set(blist))
print "..............................................."

print len(blist2), "Lenn blist"
blist2 =list(set(blist2))
print len(blist2), "lenn set"
blist2.sort()

print len(blist), "Lenn blist"
blist =list(set(blist))
print len(blist), "lenn set"
blist.sort()

print "======================================================================================================================================"
#print "BLI:",blist2
print "--------------------------------------------------------------------------------------------------------------------------------------"

'''
bigb=[]
dips = set(blist)
for b in dips:
    j=b
    for _ in [':_',': ',' :','_:']:
        j=j.replace(_,'')
    if not (':' in j or '(page does not exist)' in j):
        bigb.append(b)
print "&",len(bigb)
'''
#keyz.sort()
skeyz = set(keyz)
keyz = list(skeyz)
print len(keyz)
keyz.sort()
blat.sort()
print "LKS", len(keyz)
print "Lblat", len(blat)
print keyz[-1]
MM = numpy.zeros(shape=(len(keyz),len(blat)), dtype=numpy.dtype('uint8'))
PP = numpy.zeros(shape=(len(keyz),len(keyz)), dtype=numpy.dtype('float'))
NN = numpy.zeros(shape=(len(keyz),len(blat)), dtype=numpy.dtype('uint8'))
#PP = numpy.zeros(shape=(len(keyz),len(blat)), dtype=float)
#print MM


for sk in range(0,len(keyz)):
    if keyz[sk] in bdic:
        for link in bdic[keyz[sk]]:
            if link in keyz:
                MM[sk][blat.index(link)]=1
print "LENN",len(MM),len(keyz)

numpy.savetxt("HMunMM.csv", MM, delimiter=",")

#outt = open(path+'outt.txt', 'w')

print "lengths", len(MM), len(MM[0])

#for m in range(len(MM)):
#    print keyz[m]

print "vvvvvvvvvvvvvvvvvv"

#for m in range(len(MM[0])-9997):
#    print blat[m]


#numpy.savetxt("Mam.csv", MM, delimiter=",")


for m in range(len(MM)):
    print keyz[m]

    for n in range(m):
        print n,m,'|',
        #print "Xi:",bdic[keyz[n]]
        PP[m][n]=1-(len(set(bdic[keyz[m]]).symmetric_difference(set(bdic[keyz[n]]))) /float(max(1,len(set(bdic[keyz[m]])) +len(set(bdic[keyz[n]])))))
        PP[n][m]=PP[m][n]
        #print PP[m][n],


numpy.savetxt("HMunPP.csv", PP, delimiter=",")

print "Now MM done"

for m in range(len(MM)):
    #print keyz[m]

    #print keyz[m]
    for n in range(len((MM[0]))):
        NN[m][n]=len(set(bdic[keyz[m]])&set(bdic[keyz[n]]))
        NN[n][m]=NN[m][n]
        #print PP[m][n],

numpy.savetxt("HMunNN.csv", NN, delimiter=",")


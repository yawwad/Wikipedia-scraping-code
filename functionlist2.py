import calendar
import numpy
import requests
import math
from bs4 import BeautifulSoup
import datetime as dt

def linkTranslate(title, lang1, lang2):
    #print "T:"+title,
    url = 'https://'+lang1+'.wikipedia.org/w/api.php?action=query&format=json&titles='+title+'&prop=langlinks&lllimit=500' #??? 'title'
    r = requests.get(url)
    if 'query' not in r.json():
        return ""
    query = r.json()['query'] #['pages'].values()
    if 'pages' in query:
        pages = query['pages'].values()
    else:
        return ""
    page = pages[0]
    entit=""
    if 'langlinks' in page:
        for lang in page['langlinks']:
            if lang['lang']==lang2:
                return lang['*']
            if lang['lang']=='en':
                entit = lang['*']
        #langs[lang['lang']] = lang['*'] #name in that language
    print "ANT",
    '''
    if lang1 is not 'en' and len(entit)>0:
        url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&titles='+entit+'&prop=langlinks&lllimit=500' #??? 'title'
        r = requests.get(url)
        page = r.json()['query']['pages'].values()
        page = page[0]
        entit=""
        for lang in page['langlinks']:
            if lang['lang']==lang2:
                return lang['*']
    print "retQ",
    '''
    return ""

def linksTranslate(sett, lang1, lang2):
    ret = list()
    for i in sett:
        if len(i)>0:
            ret.append(linkTranslate(i, lang1, lang2))
    return set(ret)

def linkripper(url, lang, title, twisto):
    ret = {}
    Ti=unicode(title)
    La=lang
    tilang=unicode(Ti)+':'+La
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        div = soup.find('div', { "id" : "mw-content-text" })
        #allall = div.findAll('a',attrs = {'title' : True})
        allall = div.findAll('p')
            
        for p in allall:
            linx=p.findAll('a',attrs = {'title' : True})
            for ay in linx:
                wlink=ay.get('title')
                #print wlink,
                
                try:           
                    ret[twisto[wlink+':'+unicode(La)]]=wlink #We care existence
                    #print '*|',
                except KeyError:
                    pass
                    #print '#|',
        #print ""
    except:
        print "twister error in ",tilang                
    return ret                


def linkripperII(url, lang, title, twisto):
    ret = {}
    Ti=unicode(title)
    La=lang
    tilang=unicode(Ti)+':'+La
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        div = soup.find('div', { "id" : "mw-content-text" })
        allall = div.findAll('a',attrs = {'title' : True})
                
        for ay in allall:
            wlink=ay.get('title')
            kko=wlink+':'+unicode(La)
            
            try:           
                ret[twisto[wlink+':'+unicode(La)]]=wlink #We care existence
                #print wlink,'|',
            except KeyError:
                '''
                try:
                    #url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&titles='+'title'+'&prop=langlinks&lllimit=500'
                    r = requests.get('https://'+La+'.wikipedia.org/w/api.php?action=query&format=json&titles='+wlink+'&prop=langlinks&lllimit=500')
                    
                    page = r.json()['query']['pages'].values()
                    if 'langlinks' in page.keys(): #if available in >0 languages
                        for lang in page['langlinks']:
                            if lang['lang']=='en':
                                ret[twisto[lang['*']+':'+unicode(La)]] = wlink+'<e>' #lang['*'] 
                                print '(`'+La,wlink,')',
                                break
                        print '({'+La,wlink,')',
                except:
                    print '(~'+La,wlink,')', 
                '''
                pass
    except:
        print "twister error in ",tilang                
    return ret                 


def linkripTitles(url):#, lang, title):
    ret = {}
    #tilang=unicode(Ti)+':'+La
    if '#' in url:
        return linkripTitles2(url[:url.index('#')],url[url.index('#')+1])
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')        
        div = soup.find('div', { "id" : "mw-content-text" })
        
        stri="mw-content-text"
        stri = "<span class=\"mw-headline\" id=\"References\">References</span>"
        

        #comment-out this
        
        
        mystr = str(div)
        flag = 'id=\"toc\"'
        #flag = '>References<'
        
        if flag in mystr:
            mystr = mystr[mystr.index('<p>'):mystr.index(flag)]
            mystr = mystr[mystr.index('<p>'):mystr.rfind('<')]
            #print "----------------------------------------\n",url,mystr,"\n----------------------------------------"
            div = BeautifulSoup(mystr,'html.parser')
        
        
        
        #allall = div.findAll('a',attrs = {'title' : True})
        allall = div.findAll('p')
            
        for p in allall:
            linx=p.findAll('a',attrs = {'title' : True})
            for ay in linx:
                wlink=ay.get('title')
                #print wlink,
                
                try:           
                    ret[wlink]=True #We care existence
                    #print '*|',
                except KeyError:
                    pass
                    #print '#|',
        #print ""
    except:
        print "twister error in ",url
        #ret = linkripTitles(url)
    return ret

def linkripTitless(url):#, lang, title):
    ret = {}
    #tilang=unicode(Ti)+':'+La
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')        
        #div = soup.find('div', { "id" : "mw-content-text" })
        #div=soup
        print str(div)[:10000]
        #HERE WE GO
        #div = soup.find('div', { "class" : "mw-parser-output" })
        

        headlines = div('span', {'class' : 'mw-headline'})
        heads = [_.text for _ in div('span', {'class' : 'mw-headline'})]
        print "<<<<<"+str(headlines[0])+">>>>>"

        #comment-out this
        #print "#short#",
        print 'okee here'
        mystr = str(div)
        flag = 'id=\"toc\"'
        #flag = '>References<'
        
        if flag in mystr:
            mystr = mystr[:mystr.index(flag)]
            print 'hey yo'
            mystr = mystr[mystr.index('<p>'):mystr.rfind('<')]
            print "----------------------------------------\n",url,mystr,"\n----------------------------------------"
            div = BeautifulSoup(mystr,'html.parser')
        
        #allall = div.findAll('a',attrs = {'title' : True})
        print "XXXXX"
        print div.findAll('table')
        print "ZZZZZ"
        allall = div.findAll(['div','ul','table','p'])
        print type(allall)
        print [type(_) for _ in allall]
            
        for p in allall:
            linx=p.findAll('a',attrs = {'title' : True})
            print "LENN",len(linx)
            for ay in linx:
                wlink=ay.get('title')
                #print wlink,"*",
                
                try:           
                    ret[wlink]=True #We care existence
                    #print '*|',
                except KeyError:
                    pass
                    #print '#|',
        #print ""
    except:
        print "twister error in ",url
        #ret = linkripTitles(url)
    return ret
    
def linkripTitlesL(url):#, lang, title):
    ret = {}
    #tilang=unicode(Ti)+':'+La
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')        

        div = soup.find('div', { "id" : "mw-content-text" })
        
        
        #allall = div.findAll('a',attrs = {'title' : True})
        #allall = div.findAll(['ul','table','p'])
        
        mystr = str(div)
        #print "linn",len(mystr),
        flag = '>References'
        #print '                                      YYYYYYYYYYYY     flag:',flag
        if flag in mystr:
            mystr = mystr[mystr.index('<p>'):mystr.rindex(flag)]

            mystr = mystr[mystr.index('<p>'):mystr.rfind('<')]
            
            #print "----------------------------------------\n",url,mystr,"\n----------------------------------------"
            div = BeautifulSoup(mystr,'html.parser')
        
        allall = div.findAll(['div','ul','table','p'])
        
        for p in allall:
            linx=p.findAll('a',attrs = {'title' : True})
            for ay in linx:
                wlink=ay.get('title')
                #print wlink,
                
                try:           
                    ret[wlink]=True #We care existence
                    #print '*|',
                except KeyError:
                    pass
                    #print '#|',
        #print ""
    except:
        print "twister error in ",url
        #ret = linkripTitles(url)
    return ret

def linkripTitles2(url,section):#, lang, title):
    ret = {}
    #tilang=unicode(Ti)+':'+La
    try:
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')         
        mystr = str(soup)

        headlines = soup('span', {'class' : 'mw-headline'})
        heads = [_.text for _ in soup('span', {'class' : 'mw-headline'})]

        for h in range(len(heads)):
            if heads[h]==section:
                
                flag = headlines[h]

                if str(flag) in mystr:
                    mystr = mystr[mystr.index(str(flag))+len(flag):mystr.rindex(str(headlines[h+1]))]
        
                    mystr = mystr[:mystr.rfind('<')]

                    div = BeautifulSoup(mystr,'html.parser')

                else:
                    raise Exception('x should not exceed 5. The value of x was: {}'.format(x))
                break
                
        
        '''
        print "***"
        for headline in soup('span', {'class' : 'mw-headline'}):
            #print headline.text,
            if headline.text==section:
                print headline.find_next('ul').find_all('a')
        '''

        #print div
        allall = div.findAll(['div','ul','table','p'])
        #allall = div.findAll('a',attrs = {'title' : True})
        #print "haiii2",allall
        #print [_.get("title") for _ in allall]  #"href" changed from "title"
        
        for p in allall:
            linx=p.findAll('a',attrs = {'title' : True})
            for ay in linx:
                wlink=ay.get('title')
                
                try:           
                    ret[wlink]=True #We care existence
                    #print '*|',
                except KeyError:
                    pass
                    #print '#|',
        #print ""
    except:
        print "twister error in ",url
        #ret = linkripTitles(url)
    return ret


def tupler(x,y):
    return tuple([tuple(["" for _ in range(y)]) for _ in range(x)])

def mergeDic(dic1,dic2):
    #dicc2=dict(dic2)
    for d in dic1:
        if d in dic2:
            dic1[d]=list(set(dic1[d])|set(dic2[d]))
            del dic2[d]
    for d in dic2:
        dic1[d]=dic2[d]


def matricize(dicti, keyz):
    #keyz = list(set(dicti.keys()))
    #keyz.sort()
    #bkeys=set()
    
    #for d in keyz:
    #    bkeys=bkeys|set(dicti[d])|set([d])
    

    #bkeys=bkeys-set(keyz)
    #bkeys=list(bkeys)
    #wikiclean(bkeys)
    #bkeys.sort()
    #bkeys=keyz+bkeys
    ss = numpy.zeros((len(keyz), len(keyz)), dtype=numpy.int8)
    
    for d in range(len(keyz)):
        for e in dicti[keyz[d]]:
            if e in keyz:
                ss[d][keyz.index(e)]=1
    
    return (keyz,ss)


def matricizeB(dicti, keyz):
    #keyz = list(set(dicti.keys()))
    #keyz.sort()
    #dicti=dict()
    #for d in dicto:
    #    dicti[unicode(d)]=dicto[d]
    bkeys=set()
    
    for d in keyz:
        bkeys=bkeys|set(dicti[d])|set([d])
    

    bkeys=bkeys-set(keyz)
    bkeys=list(bkeys)
    bkeys=keyz+bkeys
    wikiclean(bkeys)
    bkeys.sort()

    
    ss = numpy.zeros((len(bkeys), len(bkeys)), dtype=numpy.int32)
    for d in range(len(bkeys)):
        #print [bkeys[d]],[unicode(bkeys[d])]
        #dicti[bkeys[d]]
        dicti[unicode(bkeys[d])]

        bkeys[d]
        dicti[bkeys[d]]
        li=list(set(dicti[bkeys[d]])&set(bkeys))
        for e in li:
            ss[d][bkeys.index(e)]=1
    
    return (keyz,bkeys,ss)



#def getMatrix(dictio):
#    return getMatrix(dictio,dictio.keys())

def list2file(list,file):
    with open(file, 'w') as f:
        for item in list:
            f.write("%s\n" % item.encode("utf-8"))
def wikiclean(liss):
    lenb=len(liss)
    for k in range(0, lenb):
        j=liss[lenb-1-k]
        for _ in [':_',': ',' :','_:']:
            j=j.replace(_,'')
        if ':' in j or '(page does not exist)' in j:
            del liss[lenb-1-k]
    
def getMatrix(dictio, labels):
    #arr = numpy.empty((len(labels), len(labels)), dtype=str)
    
    arr=[[] for _ in labels]
    
    for a in arr:
        a = [[] for _ in labels]
    #keyz=dictio.keys()
    lenn=len(labels)
    print "KK",labels
    for i in range(lenn):
        for j in range(i):
            if not (labels[j] in dictio and labels[i] in dictio):
                for k in [i,j]:
                    if labels[k] not in dictio:
                        dictio[labels[k]]=linkripTitles('https://en.wikipedia.org/wiki/'+labels[k]).keys()
                simm=set(dictio[labels[j]]) & set(dictio[labels[i]])
                simm=list(simm)
                simm.sort()
                arro=""
                for s in simm:
                    arro=arro+s+'|'
                print labels[i],labels[j]+':',len(simm)
            #arr[i][j]=arro
            #arr[j][i]=arr[i][j]
    #return arr

def getMatrixL(dictio, labels):
    arr = numpy.zeros((len(labels), len(labels)), dtype=numpy.int32)
    #keyz=dictio.keys()
    lenn=len(labels)
    print "KK",labels
    for i in range(lenn):
        for j in range(i):
            simm=set(dictio[labels[j]]) & set(dictio[labels[i]])
            arr[i][j]=len(simm)
            arr[j][i]=arr[i][j]
    return arr

def getMatrixS(dictio, labels):
    arr = numpy.zeros((len(labels), len(labels)), dtype=float)
    #keyz=dictio.keys()
    lenn=len(labels)
    #print "KK",labels
    for i in range(1,lenn):
        for j in range(i):
            simm=set(dictio[labels[j]]) & set(dictio[labels[i]])
            simm=list(simm)
            simm.sort()
            arr[i][j]=len(simm)/math.sqrt(max(1,len(dictio[labels[j]])*len(dictio[labels[i]])))
            arr[j][i]=arr[i][j]
    return arr
def dayscount(timestamp):
    year = int(timestamp.split('-')[0])
    month = int(timestamp.split('-')[1])
    day = int(timestamp.split('-')[2][:2])
    clock = timestamp.split('T')[1]
    hour = clock.split(':')[0]
    min = clock.split(':')[1]
    sec = clock.split(':')[2][:2]

    monthdays = 0
        
    for m in range(1,int(month)):
        monthdays = monthdays+calendar.monthrange(int(year),m)[1] #"looop","month",m,monthrange(int(year),m)[1]    
 
    days = ((year-2012)*365) +calendar.leapdays(2012,year)+ monthdays + day - 1 + float(hour)/24 + float(min)/(24*60) + float(sec)/(24*3600)
    return days

def dayscount2(timestamp):
    year = int(timestamp.split('-')[0])
    month = int(timestamp.split('-')[1])
    day = int(timestamp.split('-')[2][:2])
    clock = timestamp.split(' ')[1]
    hour = clock.split(':')[0]
    min = clock.split(':')[1]
    sec = clock.split(':')[2][:2]

    monthdays = 0
        
    for m in range(1,int(month)):
        monthdays = monthdays+calendar.monthrange(int(year),m)[1] #"looop","month",m,monthrange(int(year),m)[1]    
 
    days = ((year-2012)*365) +calendar.leapdays(2012,year)+ monthdays + day - 1 + float(hour)/24 + float(min)/(24*60) + float(sec)/(24*3600)
    return days    
def daysstamp(days):
    year = 2012 + int(days/365)
    monthdays = days%365 - calendar.leapdays(2012, year)
    #print year, monthdays, 'yea'
    month=1
    #print 'cc',calendar.leapdays(2012, year)
    while monthdays>calendar.monthrange(year,month)[1]:
        monthdays = monthdays-calendar.monthrange(year,month)[1]
        #print "mm",monthdays
        month=month+1
    #print "daa",days,round(days)    
    clock = (days-int(days))*24
    mins = (clock-int(clock))*60
    secs = str(int((mins-int(mins))*60))
    day = str(int(monthdays)+1)
    
    clock = str(int(clock))
    mins = str(int(mins))
    
    month = str(month)
   
    if len(month)<2:
        month = '0'+month        
    if len(day)<2:
        day = '0'+day
    if len(clock)<2:
        clock='0'+clock
    if len(mins)<2:
        mins='0'+mins
    if len(secs)<2:
        secs='0'+secs
    
        
    return str(year)+'-'+month+'-'+day+'T'+clock+':'+mins+':'+secs+'Z'

def revidhistory(lang,title):#, finalList):
    revos = []
    halt = False
    url = 'https://'+lang+'.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=' +title+'&rvlimit=500&rvdir=newer'
    #print "yoyo"
    while not halt:
        try:
            #print "HI-0",
            r = requests.get(url)
            #print "HI-1",
            if 'continue' in r.json():
                rvcontinue = r.json()['continue']['rvcontinue']
                #print "RVCONT:",rvcontinue
            
            if 'batchcomplete' in r.json(): #['batchcomplete'] == '':
                halt = True
            else:
                url = 'https://'+lang+'.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=' +title+'&rvlimit=500&rvdir=newer&rvcontinue='+rvcontinue
            revos.append(r.json()['query']['pages'].values()[0]['revisions'])
            #print "HI-3",rvcontinue
            
    
        except Exception as ee:
            print "s",ee.args[0]
            print ee
            break
    
    
    
    mast=[]
    
    for i in revos:
        #print i[len(i)-1]
        for j in i:
            mast.append((j['timestamp'],j['revid']))
        
    #print "<><><><><><><><><><><><><><><><><><><><>"
    #for m in range(len(mast)):
    #    print m,mast[m]
    return mast

def getOldID(lang, title, date):
    revos = revidhistory(lang,title)
    start=0
    end=len(revos)-1
    if end<0:
        return -1
    while(True):
        if start==end:
            if revos[start][0][:len(date)]==date:
                return revos[start][1]
            else:
                print "date not found for",date,"|",title, ". Instead date="+revos[start][0]
                return revos[start][1]
        tdate=int((end+start)/2)
        #print 'tdate',tdate, "len(revos)",len(revos)
        if revos[tdate][0][:len(date)]>=date:
            end=tdate
        else:
            start=tdate+1
        


def LH(lang,title):
    return realLH(lang,title,revidhistory(lang,title))

def realLH(lang,title, revos):#, finalLinks):
    n = int( math.log(len(revos),2) ) #log stepsize
    lis = dict()
    #print "CC",revos[-1][1]
    #print "DD",revos[len(revos)-1][1]
    #nested loop: iterate n, then iterate each 2-step til reaching end (well, you actually start at the end to avoid index issues)
    firstID = revos[0][1]
    firstdate = revos[0][0]
    print "Firsts:",firstID, firstdate
    
    lis[revos[0][1]]=set(linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?oldid='+str(revos[0][1])))    
    lis[revos[(2**n)-1][1]]=set(linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?oldid='+str(revos[pow(2,n)-1][1])))
    lis[revos[-1][1]]=set(linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?oldid='+str(revos[-1][1])))    
    
    print "Addded",revos[0][1],revos[(2**n)-1][1],revos[-1][1]
    print "Addded",0,(2**n)-1,len(revos)-1
    print "##### LENGTHS #####:",len(lis[revos[0][1]]),len(lis[revos[(2**n)-1][1]]),len(lis[revos[-1][1]])
    print revos[0][1],revos[(2**n)-1][1],revos[-1][1]
    
    print lis[firstID]
    pre = lis[revos[0][1]]
    if len(set(lis[revos[-1][1]])-set(lis[revos[pow(2,n)-1][1]]))==0:
        #print "About to slice I",pow(2,n)-1,"and end"
        revos = revos[0:pow(2,n)]
    if len(set(lis[revos[pow(2,n)-1][1]])-set(pre))==0:
        pre = set(lis[revos[pow(2,n)-1][1]])
        #print "About to slice II"
        revos = revos[pow(2,n):len(revos)] #Then do the same for the other n's, keeping in mind you're no longer limited to 2 (but instead 4, 8 etc.)
    n = int( math.log(len(revos),2) ) #log stepsize
       
    for i in range(n):
        m = n-i-1  #From n to 1 (now n-1 to 0) !!!!!!!!!!
        top = len(revos) - len(revos)%pow(2,m)
        prevtop = len(revos) - len(revos)%pow(2,m+1)
        blocks = prevtop/pow(2,m+1)
        if top>prevtop:
            lis[revos[top-1][1]]=set(linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?oldid='+str(revos[top-1][1])))
            print 'Addded2', revos[top-1][1], "which is",top-1
            if len(set(lis[revos[top-1][1]])-set(lis[revos[prevtop-1][1]]))==0:
                #print "SLICE 1"
                revos = revos[0:prevtop]
            
        for j in range(blocks-1):
            block = blocks-j #from blocks to 1 (now 2)
            hi = (block*pow(2,m+1))
            
            lo = (block-1)*pow(2,m+1)
            mid = (block*pow(2,m+1)) - pow(2,m)

            
            lis[revos[mid-1][1]] = set(linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?oldid='+str(revos[mid-1][1])))
            print "Addded3",revos[mid-1][1], "which is",mid-1

            if len( set(lis[revos[hi-1][1]])-set(lis[revos[mid-1][1]]) )==0:
                revos = revos[0:mid]+revos[hi:len(revos)]
                
            if len( set(lis[revos[mid-1][1]])-set(lis[revos[lo-1][1]]) )==0:
                print "SLICE 21: LEN", len(revos),"mid=", mid, "lo=",lo

                revos = revos[0:lo]+revos[mid:len(revos)]
                
        hi = pow(2,m+1)
        lo = pre 


        mid = pow(2,m)
        lis[revos[mid-1][1] ] = set(linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?oldid='+str(revos[mid-1][1])))
        print "Addded4",revos[mid-1][1],"which is",mid-1

        if len(set(lis[revos[hi-1][1]])-set(lis[revos[mid-1][1]]))==0:
            print "sliced",revos[mid][1],"to",revos[hi][1], "which are:",mid,hi
            revos = revos[:mid]+revos[hi:len(revos)]            
        
        if len(set(lis[revos[mid-1][1]])-lo)==0:
            revos = revos[mid:len(revos)]       
        
        print "lenn", len(revos)
        
    print lang,"CLOSING:-",dt.datetime.now()
    

    w = lis[revos[0][1]]
    c=0
    az=[]
    if len(lis[firstID])>0:
        az.append([firstdate , firstID, lis[firstID]])
    print "{{{{{{{",az,"}}}}}}}"
    az.append([revos[0][0], revos[0][1], list(w-lis[firstID])])
    print "<<<<<",revos[0][0], revos[0][1], list(w),">>>>>"
    print "&& (",revos[0][0],revos[0][1],")",w,"&&"
    url = 'https://'+lang+'.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles='+title+'&rvlimit=1&rvdir=newer'
    r = requests.get(url)
    oid = r.json()['query']['pages'].values()[0]['revisions'][0]['revid']
    time = r.json()['query']['pages'].values()[0]['revisions'][0]['timestamp']
    
    print "OID:",oid, "\tTIME:",time
    u = set(linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?oldid='+str(oid)))
    print "DIFF:", w-u  
    print "DIFF:", u-w
    for r in revos[1:]:
        x = lis[r[1]]
        az.append([r[0],r[1],list(x-w)])
        w=x
        
    print "CLOSING:^",dt.datetime.now()
    return az
                         
def dateMe(lang,title, link):
    low=0
    mast = revidhistory(lang,title)
    print "mast length",len(mast)
    high = len(mast)
    
    loTitles = linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?title='+title+'&oldid='+str(mast[low][1])).keys()
    midTitles= linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?title='+title+'&oldid='+str(mast[low + int((high-low)/2) ][1])).keys()
    loTitles.sort()
    midTitles.sort()
    print loTitles
    print midTitles    
    hiTitles=linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?title='+title+'&oldid='+str(mast[high-1][1])).keys()
    hiTitles.sort()
    print hiTitles            
    
    '''
    if link not in set(hiTitles):
        return -1
    else:
        print "Good stuff",link
    '''
    
    while high-2>low:  
        mid = low + int((high-low)/2) 
        
        loTitles = linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?title='+title+'&oldid='+str(mast[low][1])).keys()
        midTitles= linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?title='+title+'&oldid='+str(mast[mid][1])).keys()
        hiTitles = linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?title='+title+'&oldid='+str(mast[high-1][1])).keys()
 
        if link in set(loTitles):
            print "LOWW",low, mast[low][0]
            return low
        elif link in set(midTitles):
            print "Ceiling is: #:",mid, mast[mid][0]
            high=mid+1
        elif link in set(hiTitles):
            print "Floor is#"+str(mid), mast[mid][0]
            low = mid
        
    if high-2==low: #down to 2 spots, low and high-1
        print "i"
        loTitles = linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?title='+title+'&oldid='+str(mast[low][1])).keys()
        hiTitles = linkripTitles('https://'+lang+'.wikipedia.org/w/index.php?title='+title+'&oldid='+str(mast[high-1][1])).keys()
        link = unicode(link)
        
        if link in set(hiTitles):
            print "Time:",str(mast[high-1][0])
            return high-1
        elif link in set(loTitles):
            print "Time:",str(mast[low][0])
            return low
    elif high-1==low:
        print "i"
        print "Timc:",str(mast[low][0])
        return low
    else:
        print "i"
        return -1
        
  
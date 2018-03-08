##Author: Rashmi Varma
##Created: September 28, 2017
##Career and Job Center Agent
##Agent accepts a list of free-form keywords from the command line and outputs Career 
##and job opportunities that closely match the input keywords. Agent uses 
##k-nearest neighbor algorithm to find matches for any given value of k.

libnames = ['math', 'os', 'operator','matplotlib', 'matplotlib.pyplot']
for libname in libnames:
    try:
        lib = __import__(libname)
    except:
        print ("One of the required libraries has not been installed. Please install %s" ,lib)
try:
    from bs4 import BeautifulSoup

except:
    print("\nCould not import Beautiful Soup library")
try:
    import urllib2
except:
    print("\nCould not import UrlLib2")
try:
    import os.path
except:
    print("\nCould not import os path")
try:
    import csv
except:
    print("\nCould not import csv")

##Checks if the input keyword is present in the dictionary, if not it scrapes 
##from websites. 
##If input present, it fetches the links associated with the keyword.
def clusterFunc(key):
    clusterData = {}
    try:
        filename = 'Dictionary.csv'
        with open(filename,'rb') as infile:
            reader = csv.reader(infile,dialect='excel')
            rows = reader.next()
            if(rows[1]==key):
                print("Keyword present in lookup file")
            for rows in reader:
                clusterData['title'] = rows[1]
                clusterData['content'] = rows[4]
                clusterData['link'] = rows[2]
                agent(key, '0')
                infile.close()
    except:
        print("The lookup table has no data. Please perform a search on Step 2 to populate the table")
    

##Compares the index of the sliced down Jaccard values according to k, 
##to their position in the link's list. This makes finding the 
##appropriate link to display easier
def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

##def sendToScreen(d,knn_k,link):
##    for i in range(0,knn_k):
##        index = d[i]
##        print(link[index])
##        links = link[index]
##        print('<a href="{0}">{0}</a>'.format(link))

##Actuator computes which documents are closest to our keyword and retrieves them
def actuator(k1,link, k):
##    l = len(k1)
    d=[]
    d1=[]
    knn_k = int(k)
    orderedJacc = sorted(k1)
    takingK = []
##    for x in range(0,k):
    takingK = (orderedJacc[:k])


    for x in range(0,len(link)):
        for k in takingK:
            d.append(list_duplicates_of(k1,k))
    count=0
    for everyd in range(0,len(d)):
        if count==knn_k:
            break;
        else:
            dnd=d[everyd]
            for nn in dnd:
                d1.append(nn)
        if len(d1)==knn_k:
            break
        else:
            links = link[nn]
            print ("\n",links)
        count=count+1

    
#Here, we calculate Jaccard's distance and send it back to the Analysis 
##function of the agent
##  http://journocode.com/2016/03/10/similarity-and-distance-part-1/

def JacCal(str1, str2, lenFreq, lenLink, lenKey):
    num = float(str1)
    den = float(lenKey + lenLink)
    deno = den - num
    j = num/den
    j = 1 - j
    j = j*100
    j = round(j,2)
    return j

##This function sends data from agent about frequency to our 
##function which computes Jaccard's distance
def frequencyAnalysis(freq, link, freqLength, lenLink,key,k):
    k1 = []
    for x in range(0,freqLength):
        str1 = freq[x]
        str2 = link[x]
        jacc = JacCal(str1, str2, freqLength, lenLink, len(key))
        k1.append(jacc)
    actuator(k1, link,k)
        
##Agent computes all the details. Agent reads details from our table and computes 
##frequency of the keyword's occurence in our retreieved links
def agent(key,k):
    filename = 'Dictionary.csv'
    title = []
    content = []
    link = []
    freq = []
    index = 0
    ind = []
    with open(filename,'rb') as infile:
        reader = csv.reader(infile,dialect='excel')
        rows = reader.next()
        for rows in reader:
            title.append(rows[1])
            content.append(rows[4])
            link.append(rows[2])
        lenTitle = len(title)
        lenContent = len(content)        
        lenLink = len(link)        


    infile.close()
    kk = len(key)

    for x in range(0,lenTitle):
        countC = 0
        for y in range(0,kk):
            countC = countC + content[x].count(key[y])

        freq.append(countC)
    freqLength = len(freq)
    frequencyAnalysis(freq, link, freqLength, lenLink,key,k)
 
   
##The function used to write to the file                  
def writeFile(key,title,link,src,content):
    filename = 'Dictionary.csv'
    lists = [key, title, link, src, content]
    with open(filename,'rb') as infile:
        reader = csv.reader(infile,dialect='excel')
        rows = reader.next()
        if(rows==lists):
            print("\n\nAlready present")
            infile.close()

        else:
            with open(filename,'a') as outfile:
                try:
                    writer = csv.writer(outfile,dialect='excel')
                    writer.writerow(lists)
                    outfile.close()
                except UnicodeError:
                    pass
##This function is used to retrieve the data from the URL's scrapped. 
##Every job search opens to an individual page which contains more details about it. 
##This function retrieves those details
def findContent(source, page,source_page):
    co = []
    urlPage1 = urllib2.urlopen(page)
    soup1 = BeautifulSoup(urlPage1, 'html.parser')
    urlPageIndeed = urllib2.urlopen(source_page)
    soup2 = BeautifulSoup(urlPageIndeed, 'html.parser')
    
    if source=='acm':
        for everyline in soup1.find_all('span'):
            if hasattr(everyline, "text"):
                co.append(everyline.text)
        return co
    if source=='ieee':
        for everyline in soup1.find_all('span'):
            if hasattr(everyline, "text"):
                co.append(everyline.text)
        return co
    if source == 'indeed':
        for everyline in soup2.find_all('span',{'class':'summary','itemprop':'description'}):
                if hasattr(everyline, "text"):
                    co.append(everyline.text)
        
        return co

##The scrapper is a web scrapping function which uses BeautifulSoup library
##The scrapper scraps data and saves it to the lookup table for future use
    
def scrapper(source, page,key,k):
    urlPage = urllib2.urlopen(page)
    soup = BeautifulSoup(urlPage, 'html.parser')

    if source=='acm' or 'ieee':
            for row in soup.find_all('h3'):
                if hasattr(row, "text"):
                    title = row.text
                for a in row.find_all('a', href=True):
                    links = page + a['href']
                    src = source
                    content = findContent(source, links,page)
                    writeFile(key,title,links,src,content)
                    
    if source=='indeed':
        for row in soup.find_all('a', {'target' : '_blank', 'data-tn-element' : 'jobTitle'}):
            if hasattr(row, "text"):
                title = row.text
                l = row.get('href')
                links = page + l
                src = source
                content = findContent(source, links,page)
                writeFile(key,title,links,src,content)
                
##The sensor is responsible for getting input data to the agent.
## Here, the sensor readies the URL and calls the web scrapping function
##We have currently restricted the reading to 15 values per page. This can be increased but it also increases the execution time of the program
##The program currently takes 3-4 minutes for scrapping a new keyword sequence                
                
def sensor(acm_page, ieee_page, indeed_page, keywords, k,key1):
    print("\nGathering data...")
    for everyKeyword in keywords:
        acm_page = acm_page + everyKeyword
        ieee_page = ieee_page + everyKeyword
        indeed_page = indeed_page + everyKeyword
        if len(keywords) > 1:
            acm_page = acm_page + '+' 
            ieee_page = ieee_page + '+' 
            indeed_page = indeed_page + '+'
    if len(keywords) > 1:
        acm_page = acm_page[:-1]
        ieee_page = ieee_page[:-1]
        indeed_page = indeed_page[:-1]
    acm_page = acm_page + '?rows=15'
    ieee_page = ieee_page + '?rows=15'

    scrapper('acm', acm_page,key1,k)
    scrapper('ieee',ieee_page,key1,k)
    scrapper('indeed',indeed_page,key1,k)


    
#The environment creates the url for scrapping data and sends these Url's to the sensor.
#The environment also checks if entered keyword is present in the look up table. Ideally if it is present, it won't send data to the sensor but simply read from look up table
def environment(keywords, k,key1):
    filename = 'Dictionary.csv'
    with open(filename,'rb') as infile:
        reader = csv.reader(infile,dialect='excel')
        rows = reader.next()
        if(rows==key1):
            print("\n\nAlready present")
            infile.close()

    acm_page = 'http://jobs.acm.org/jobs/results/keyword/'
    ieee_page = 'http://jobs.ieee.org/jobs/results/keyword/'
    indeed_page = 'https://www.indeed.com/jobs?q='
    sensor(acm_page, ieee_page, indeed_page, keywords, k,key1)
    agent(key1, k)
    

##  The code runs continuously till 0 is pressed to quit it. 
##On opening, the look up table gets created. If it already exists then we do nothing, 
##otherwise we create and write headers to it
##  Program can take multiple keywords as input from the user. 
##User also takes the value of k here.These values are passed to the environment
def main():
    quitFlag=False
    filename = 'Dictionary.csv'
    file_exists = os.path.isfile(filename)
    headers = ['Keyword','Title','Link','Source','Content' ]
    with open (filename, 'wb') as csvfile:
        dw = csv.DictWriter(csvfile, headers)
        dw.writeheader()
        if not file_exists:
            writer.writeheader()
            
    while quitFlag==False:
        keywords = []
        key1 = []
        keyCounter = 0

        try:
            x = int(raw_input("\nPlease select one of the options given below: \n0. Quit \n1. Find job ads \n2. Cluster\nYour choice:"))
        except:
            print("\nChoice entered is not an integer.")
            
        try:
            if x==0:
                quitFlag==True
                break
            if x==1:
                while keyCounter==0:
                    key = raw_input("\nPlease enter Job Title, keywords, etc (Separate multiple keywords by comma):")
                    if len(key) == 0:
                        print("\nPlease enter atleast one keyword to proceed")
                        keyCounter = 0
                    else:
                        keyCounter = 1
                temp_keywords=key.split(',')
                for everyKey in temp_keywords:
                    everyKey = everyKey.strip()
                    key1.append(everyKey)
                    temp = everyKey.replace(" ","+")
                    keywords.append(temp)                   
                try:
                    k = int(raw_input("\nPlease enter how many job searches you want to see at a time(k):"))
                except:
                    print("Value of number of job searches needs to be an integer only. Please run the program again and try search again")
                    break
                environment(keywords, k,key1)       
                quitFlag=False
            if x==2:
                print("Clustering")
                while keyCounter==0:
                    key = raw_input("\nPlease enter Job Title, keywords, etc (Separate multiple keywords by comma):")
                    if len(key) == 0:
                        print("\nPlease enter atleast one keyword to proceed")
                        keyCounter = 0
                    else:
                        keyCounter = 1
                temp_keywords=key.split(',')
                for everyKey in temp_keywords:
                    everyKey = everyKey.strip()
                    key1.append(everyKey)
                    temp = everyKey.replace(" ","+")
                    keywords.append(temp)    
                clusterFunc(key1)
                
            else:
                print("\nPlease input choices again")
                quitFlag=False
        except:
            print("Please enter appropriate values only")    

main()

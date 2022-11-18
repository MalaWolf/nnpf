#!/usr/bin/python3
import re, urllib
import pandas as pd
from bs4 import BeautifulSoup
import sys

maxResults=500
try:
    query = "+" + '"' + sys.argv[1] +'"'
except:
    print("bruk: "+ sys.argv[0] + " søkeord")
    sys.exit(1)

hdr =  { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' }

urlquery = urllib.parse.quote_plus(query)

# språk & tidsavgensning(df= d=day, w=week, m=month, y=year)
tidsavgrensning="d"
#print ("q=" + urlquery + "&kl=no-no&"+"df="+tidsavgrensning) #debug

req = urllib.request.Request("http://duckduckgo.com/html/?q=" + urlquery + "&kl=no-no&df=" + "tidsavgrensning", headers=hdr)

site = urllib.request.urlopen(req)
data = site.read()
soup = BeautifulSoup(data, "html.parser")

my_list = soup.find("div", {"id": "links"}).find_all("div", {'class': re.compile('.*web-result*.')})[0:maxResults]

(result__snippet, result_url) = ([] for i in range(2))

for i in my_list:
    try:
        result__snippet.append(i.find("a", {"class": "result__snippet"}).get_text().strip("\n").strip())
    except:
        result__snippet.append(None)
    try:
        result_url.append(i.find("a", {"class": "result__url"}).get_text().strip("\n").strip())
    except:
        result_url.append(None)

for item in result_url:
    print ("https://"+item)


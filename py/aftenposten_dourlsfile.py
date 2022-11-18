#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import pandas as pd
from bs4 import BeautifulSoup as Soup
import requests
import sys
import hashlib
import json

SELENIUM_SESSION_FILE = './selenium_session'
SELENIUM_PORT=9515

def build_driver():
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("--enable-file-cookies")

    if os.path.isfile(SELENIUM_SESSION_FILE):
        session_file = open(SELENIUM_SESSION_FILE)
        session_info = session_file.readlines()
        session_file.close()

        executor_url = session_info[0].strip()
        session_id = session_info[1].strip()

        capabilities = options.to_capabilities()
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=capabilities)
        # prevent annoying empty chrome windows
        driver.close()
        driver.quit() 

        # attach to existing session
        driver.session_id = session_id
        return driver

    driver = webdriver.Chrome(options=options, port=SELENIUM_PORT)

    session_file = open(SELENIUM_SESSION_FILE, 'w')
    session_file.writelines([
        driver.command_executor._url,
        "\n",
        driver.session_id,
        "\n",
    ])
    session_file.close()

    return driver

driver = build_driver()
#driver.get("https://dt.no")
#time.sleep(3)

#testing 
## end testing

# write whatever automated thing you need to do
# if you plan to re-run be sure that the actions are idempotent

def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def read_article(kilde):
    s = Soup(kilde, "html.parser")
    date_published = s.find("time", {"itemprop":"datePublished"})
    article_author = s.find("div", {"class":"hyperion-css-0"})
    fulltext=""
    for EachPart in s.select('p[class*="hyperion-css-"]'):
        fulltext = fulltext + str(EachPart.get_text())

    return date_published.get_text(),article_author.get_text(),fulltext

try:
    if os.path.isfile(sys.argv[1]):
        urlsfile=sys.argv[1]
except:
    print("oppgi path til fil med urls")
    sys.exit(1)
    
with open(urlsfile, "r") as f:
    url_lista = f.readlines()
f.close()

for url in url_lista:
    urlHash=hash_string(url)
    url_src=[(url),(urlHash)]

    driver.get(url) # Laster inn en url
    time.sleep(3) # Juster sleep-tid slik at sida har tid å laste ferdig
    source = driver.page_source # Her har vi kildekoden.
    #print (source) #debug
    #print (read_article(source)) #debug
    try:
        textfound=(url_src,) + (read_article(source))
        jsonObject=json.dumps(textfound, indent=4)
        print(jsonObject)

    except:
        print ('read-article feilet for ' + url)
        continue

    #print(source) #debug
    print(read_article(source))
    
    # Writing to sample.json
    outFile="./json/" + str(urlHash) + ".json"
    with open(outFile, "w") as outfile:
        outfile.write(jsonObject)


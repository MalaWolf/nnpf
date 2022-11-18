#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from operator import itemgetter
from datetime import datetime

#les inn alle navn fra liste

# Using readlines()
file1 = open('/home/geriksen/nnpf/navnelister/samlet_alle_unik.txt', 'r')
navneliste = file1.readlines()

# assign directory
directory = './json_old/'

#resultatliste navnesøk
NNPFfound=[]

# iterate json files in dir
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a '.json' file
    if os.path.isfile(f) and str(f)[-5:] == '.json':
        filename=str(f)
        #print(filename)
        # Opening JSON file
        f = open(filename)
        # returns JSON object as a dictionary
        data = json.load(f)
        # Closing file
        f.close()

        for navn in navneliste:
            #do shit pr navn

            body=str(data[3])
            utf8string=body.strip()
            #print(utf8string)

            if utf8string.find(navn.strip()) != -1:
                NNPFfound.append(str(navn.strip()))

        ## oppdater json, add nnpf navn og skriv fil på nytt her
        hash=data[0][1]
        url=data[0][0]
        mydate_time_str=str(data[1]).strip()
        try: 
            dateobject=datetime.strptime(mydate_time_str.replace(',',''), '%d.%m.%y %H:%M')
        except: 
            dateobject=datetime.strptime(mydate_time_str, '%d.%m.%Y %H:%M')

        journalist=data[2]
        fulltext=data[3]
        dato=str(datetime.date(dateobject))
        datokl=str(dateobject.strftime("%Y-%m-%d %H:%M"))
        
        # opprett ny dict
        datafix={'hash':hash, 'url':url, 'publisert': datokl, 'forfatter':journalist, 'articletext':fulltext, 'NNPF':NNPFfound}
        NNPFfound=[]

        jsonObject=json.dumps(datafix, indent=4)
        print(jsonObject)

        # Writing to sample.json
        outFile="./json/" + str(hash) + ".json"
        with open(outFile, "w") as outfile:
            outfile.write(jsonObject)
        outfile.close()

file1.close()


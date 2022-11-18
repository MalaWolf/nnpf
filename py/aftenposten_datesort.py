#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from operator import itemgetter
from datetime import datetime

#les inn alle navn fra liste

# Using readlines()
file1 = open('./samlet_alle_unik.txt', 'r')
navneliste = file1.readlines()

# assign directory
directory = './json/'

#resultatliste
myList=[]

# iterate file in dir
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
            #print(navn)  #print(line.strip())

            body=str(data[3])
            utf8string=body.strip()
            #print(utf8string)

            if utf8string.find(navn.strip()) != -1:
                # [0][0]=url, [0][1]hash
                # [1]=dato
                # [2]=forfatter
                # [3]=body

                myLine=str(data[1]).strip(),str(data[0][0]).strip(),data[2].strip(),"NNPF:",navn.strip()
                myList.append(myLine)
                myLine=""

                #CSV out
                #print (str(data[1]).strip(),",",str(data[0][0]).strip(),",",data[2].strip(),",","NNPF: ", navn.strip())
                ## oppdater json, add nnpf navn og skriv fil på nytt her
file1.close()

listSorted=sorted(myList, key=itemgetter(0))

for item in listSorted:
    mydate_time_str = str(item[0])
    try:
        mydate_time_obj = datetime.strptime(mydate_time_str, '%d.%m.%y %H:%M')
        print(mydate_time_obj, ";", item[1], ";","author:", item[2],";", item[3], item[4])
    except:
        print(mydate_time_str, ";", item[1], ";","author:", item[2],";", item[3], item[4])

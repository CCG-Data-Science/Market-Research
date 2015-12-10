# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 04:24:54 2015

@author: Mike
"""

import urllib
from bs4 import BeautifulSoup # For HTML parsing


url=raw_input("Enter url: ")

html=urllib.urlopen(url).read()
soup=BeautifulSoup(html)

tags=soup('a')

for tag in tags:
    print tag.get('clk', None)




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 12:02:49 2019

@author: manzar
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from selenium import webdriver
import time


urls = 'http://www.iwma.org/Member-Directory?letter='

wb = webdriver.FirefoxProfile()
wb.set_preference("javascript.enabled", True)
driver = webdriver.Firefox(wb)

alpha = []
for i in range(65, 65 + 26):
    alpha.append(chr(i))

links = []
for char in alpha:
    url = urls + str(char)
    driver.get(url)
    time.sleep(1)
    for i in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    html = driver.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, 'lxml')
    buttons = soup.findAll('a', {'class': 'button'})
    for button in buttons[4:]:
        #print(urljoin(url, button.attrs['href']))
        links.append(urljoin(url, button.attrs['href']))

name = []
for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    n = soup.findAll('span', {'id': 'ctl00_ctl00_CorePlaceHolder_DisplayPagePlaceHolder_ctl00_Listings_ctl00_ctl00_lblReadOnlyName'})[0].text
    name.append(n)
    print(n)
    #p = soup.findAll('p', {'align': 'right'})
    #print(len(p[0].contents))
    #div = soup.findAll('div', {'id': 'ctl00_ctl00_CorePlaceHolder_DisplayPagePlaceHolder_ctl00_Listings_ctl00_ctl00_FormBuilderFormReadOnly_rptrFields_ctl03_ctl00_FormField'})
    #print(len(div[0].p.contents))

file = open('assignment.csv', 'w')
header = 'Company Name, Email, Website, telephone, Fax\n'
file.write(header)
count = 0
for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    div = soup.findAll('div', {'id': 'ctl00_ctl00_CorePlaceHolder_DisplayPagePlaceHolder_ctl00_Listings_ctl00_ctl00_FormBuilderFormReadOnly_rptrFields_ctl03_ctl00_FormField'})
    email = ''
    web = ''
    number = []
    for content in div[0].p.contents:
        #print(str(content))
        
        try:
            if('@' in content.attrs['href']):
                email = content.attrs['href'].split('mailto:')[1]
        except: 
            pass
        
        try:
            if('www' in content.attrs['href']):
                web = content.attrs['href']
        except: 
            pass
       
        try:
            #print(not any(x.isalpha() for x in content.text))
            if('+' in content):
                number.append(content.replace('Fax:', ''))
                #print(content)
        except: 
            pass
        #print(content)
    
    if(len(number) == 0):
        tel = 'NaN'
        fax = 'NaN'
    elif(len(number) == 1):
        tel = number[0]
        fax = 'NaN'
    elif(len(number) == 2):
        tel = number[0]
        fax = number[1]
    
    
    if(len(email) < 5):
        email = 'NaN'
    if(len(web) < 5):
        web = 'NaN'
    
    print(number)
    file.write(name[count].replace(',', '') + ', ' + email + ', ' + web + ', ' + tel.replace('\xa0', '') + ', ' + fax.replace('\xa0', '') + '\n')
    count += 1
    
file.close()    
file = pd.read_csv('assignment.csv')







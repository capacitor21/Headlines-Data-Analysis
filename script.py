import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import date
import re


#Get and filter the hill headlines
res = requests.get("https://thehill.com/")
text = res.text
soup = BeautifulSoup(text, 'html.parser')

titles = []
for title in soup.find_all('a'):
    #If title already in list don't add
    if title.get('title') != None and title.get('title') not in titles and len(title.text.split()) > 2:
        titles.append(title.get('title'))

#Load cnn html using selenium because page is dynamic and need to get the source html
PATH = "C:\Program Files (x86)\chromedriver.exe"

opts = Options()
opts.set_headless()
browser = webdriver.Chrome(PATH, options=opts)
browser.get("https://www.cnn.com/") #run the site

cnnHtml = browser.page_source  #get the html
time.sleep(5) #Wait 5 seconds for browser to run
browser.quit()

cnnSoup = BeautifulSoup(cnnHtml, 'html.parser')
cnnTags = cnnSoup.find_all('span', class_="cd__headline-text vid-left-enabled")

cnnTitles = []
for title in cnnTags:
    if len(title.text.split()) > 2:
        cnnTitles.append(title.text)

#Get fox html and titles
res = requests.get('https://www.foxnews.com/')
foxHtml = res.text
foxSoup = BeautifulSoup(foxHtml, 'html.parser')
articles = foxSoup.find_all('h2', class_ = 'title title-color-default')

foxTitles = []
for title in articles:
    if len(title.text.split()) > 2:
        foxTitles.append(title.text)


#Load headlines to dataframe
theHillHeadlines = pd.DataFrame({'id': np.random.randint(5000, 10000000, size=len(titles)), 'headline': titles}).set_index('id')#load to dataframe
theHillHeadlines['source'] = 'The Hill'

cnnHeadlines = pd.DataFrame({'id': np.random.randint(5000, 10000000, size=len(cnnTitles)), 'headline': cnnTitles}).set_index('id')
cnnHeadlines['source'] = 'CNN'

foxHeadlines = pd.DataFrame({'id': np.random.randint(5000, 10000000, size=len(foxTitles)), 'headline': foxTitles}).set_index('id')
foxHeadlines['source'] = 'Fox'

headlines = pd.concat([theHillHeadlines, foxHeadlines, cnnHeadlines], axis=0)
headlines['date'] = date.today().strftime("%m/%d/%Y")


#Convert dataframe to csv and append to headlines.csv
csv = headlines.to_csv('headlines.csv', mode='a')
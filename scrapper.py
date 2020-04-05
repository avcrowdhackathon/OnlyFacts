# Author Vagia Tourlida
#Scrapping using BeautifulSoup library
def news_scrapper():
 import textwrap
 import requests
 from bs4 import BeautifulSoup
 import pandas as pd

 #API CALL TO Greek google news
 news_url=' https://news.google.com/rss?hl=el&gl=GR&ceid=GR:el.'
 rss_text=requests.get(news_url).text
 soup_page=BeautifulSoup(rss_text,"xml")
 def get_items(soup):
    for news in soup.findAll("item"):
        s = BeautifulSoup(news.description.text, 'lxml')
        a = s.select('a')[-1]
        a.extract()         # extract lat 'See more on Google News..' link

        html = requests.get(news.link.text)
        soup_content = BeautifulSoup(html.text,"lxml")

        # perform basic sanitization:
        for t in soup_content.select('script, noscript, style, iframe, nav, footer, header'):
            t.extract()

        yield news.title.text.strip(), str(soup_content.select_one('body').text)
 width = 80

 #Defining a dictionary for words relevant to coronavirus
 thisdict = {"κορωναϊό","κοροναϊό","COVID-19","κορονοϊό","κορωνοϊό","coronavirus"}

 titles=[]
 contents=[]

 #Initializing the first lines of the csv
# titles.append("TITLE")
# contents.append("CONTENT")

# Extracting only title and content of the articles that contain any of the words that we specify in the dictionary
 for (title,content) in get_items(soup_page):
    title = '\n'.join(textwrap.wrap(title, width))
    content = '\n'.join(textwrap.wrap(textwrap.shorten(content, 1024), width))
    
    #Filtering out the articles in which the titles does not contain any word relevant to coronavirus
    for value in thisdict:
        if title.find(value):
            titles.append(title)
        if content.find(value):
            contents.append(content)

 df = pd.DataFrame(list(zip(titles, contents)))
 print(df.iloc[8])
 df.columns = ['title', 'content']
 return df
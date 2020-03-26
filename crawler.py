# -*- coding: utf-8 -*-
'''
Web crawler to use with DriveThruRPG.com

'''

import requests
import re
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

def check_title(pattern,title,threshold=0.6):
    #Checks if examined title is close enough to what we are searching for
    #INPUT: pattern - pattern we`re looking for, title - title to examine
    #       threshold - minimum similarity level
    #OUTPUT: True if similarity is above threshold, False if not

    if SequenceMatcher(None,pattern,title).ratio() >= threshold:
        return True
    
    else:
        return False

    


class DTCrawler():

    def __init__(self, url = 'https://www.drivethrurpg.com/', 
                 search_url = 'https://www.drivethrurpg.com/browse.php?keywords=',
                 title = 'Pierdycja' ):
        self.url = url
        self.search_url = search_url
        self.title = title
        self.links = []

    def getPages(self):
        #Opens searchpage and returns links to product pages

        links = []
        this_url = self.search_url + "+".join(self.title.split())

        try:
            req = requests.get(this_url)
        
        #Add exception handling here, with error codes and stuffs 
        except requests.exceptions.RequestException:
            return None

        site = BeautifulSoup(req.text, 'html.parser')

           
        for link in site.find_all('a',
                 {'href' : re.compile('https://www.drivethrurpg.com/product/'),
                 'title' : True}):
                      
            if check_title(self.title,link.attrs['title']):
            
                links.append(link.attrs['href'])

        self.links = links

        return links

    def get_attributes(self, url):
        #Function to get attributes (author, title, etc.) of a book on DTRG
        #INPUT: url - link to product site
        #OUTPUT: attrs - dictionary of attributes
        
        attrs = {}
        req= requests.get(url)

        site = BeautifulSoup(req.text, 'html.parser')

        for item in zip(site.find_all('div',{'class' : 'widget-information-item-title'}),site.find_all('div',{'class' : 'widget-information-item-content'})):
            attrs[item[0].text] = item[1].text

        for item in site.find_all('span', {'itemprop' : 'name'}):
            attrs[' Title '] = item.text

        for item in site.find_all('meta', {'itemprop' : 'name'}):
            attrs[' Publisher '] = item.attrs['content']

        print(attrs)
            
        return attrs     


        
     


if __name__ == "__main__":
    
    testowy = DTCrawler(title='Tales from the loop')
    print(check_title('Tales from the loop', 'Tales from the Loop RPG: Rulebook'))
    print(SequenceMatcher(None,'Tales from the loop', 'Tales from the Loop RPG').ratio())

    testowy.getPages()

    for link in testowy.links:

        print(link)
        testowy.get_attributes(link)
    
    pass

    

        



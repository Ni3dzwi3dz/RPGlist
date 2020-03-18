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

    def getPage(self):
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
            
         
            print(link.attrs['title'])
          
            if check_title(self.title,link.attrs['title']):
            
                links.append(link.attrs['href'])


      
        print(links)
        print(len(links))

        


if __name__ == "__main__":
    
    testowy = DTCrawler(title='Tales from the loop')
    print(check_title('Tales from the loop', 'Tales from the Loop RPG: Rulebook'))
    print(SequenceMatcher(None,'Tales from the loop', 'Tales from the Loop RPG').ratio())

    testowy.getPage()
    
    pass

    

        



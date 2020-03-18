# -*- coding: utf-8 -*-
'''
Web crawler to use with DriveThruRPG.com
'''

import requests
import re
from bs4 import BeautifulSoup

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
        
        except requests.exceptions.RequestException:
            return None

        site = BeautifulSoup(req.text, 'html.parser')

        #Do tego dopisz if-a ze sprawdzeniem link.attrs['title']
        #za pomocą funkcji spoza klasy
        #Taka funkcja check_title(title, attr) zwraca bool-a
        
        for link in site.find_all('a',
                 {'href' : re.compile('https://www.drivethrurpg.com/product/'),
                 'title' : True}):
            
            if check_title(title,link.attr['title']):
                links.append(link.attrs['href'])


      
        print(links)
        print(len(links))

        


if __name__ == "__main__":
    
    testowy = DTCrawler(title='Tales from the loop')

    testowy.getPage()
    
    pass

    

        



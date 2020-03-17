# -*- coding: utf-8 -*-
'''
Core file of RPGList. Includes main functionalities of the project:
-creating the list of files in specified directories
-detecting if they are e-books   
-adding them to list
-saving to .csv file

TODO:
-GUI
-different language versions
-option to add/exclude formats
-save_settings()
-find_duplicates()

Book class:
-DTRPG Parser
-Allow adding attributes


save_to_csv:
    -check if file exists, confirm to overwrite
    -Open to append, if file has headers, do not write them
    -change directory/path to file
    -prompt for filename
'''

from os import listdir
from os.path import join, isfile, splitext, basename, getsize
from csv import DictWriter, DictReader
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
from re import findall


#List of e-books extensions to be considered
extensions = ['.lrf','.lrx','.cbr','.cbz','.cb7' '.cbt','.cba','.chm','.djvu',
'.doc', '.docx','.epub','.pdb','.fb2','.xeb','.ceb','.htm','.html','.ibooks',
'.inf','.azw','.azw3','.kf8','.kfx','.lit','.prc','.mobi','.pkg','.opf','.pdf',
'.txt','.pdb','.ps','.rtf','.pdg','.xml','.tr2','.tr3','.oxps','.xps''.odt']


class Book():
    # Represents a single book in a collection

    def __init__(self,path,size=0):
        #Attributes is a dictionary, in order to allow user to add her
        #own attributes
        self.attributes = {}
        self.attributes['path']= path
        self.attributes['file'] = splitext(basename(self.attributes['path']))[0]
        self.attributes['format']=splitext(basename(self.attributes['path']))[1]

        self.attributes['title'] = ' '.join(findall(r"[\w']+", 
                                            self.attributes['file']))
        self.attributes['system'] = ''
        self.attributes['year'] = 0
        self.attributes['publisher'] =''
        self.attributes['size']= size
    
    def pdf_read(self):
        #Reads additional attributes from PDF XMP metadata and assigns them to
        #self.attributes
        
        if self.attributes['format']=='.pdf':
            
            reader = PdfFileReader(self.attributes['path'])

            self.attributes['pages'] = reader.getNumPages()

            info = reader.getDocumentInfo()

            if info:
                if info.author:
                    self.attributes['author'] = info.author
                if info.title:
                    self.attributes['title'] = info.title
        
        pass

    def DTRPG_check(self):
        #Checks if the file is sold on DriveThruRPG.com. If yes, the attributes
        #are read from page and updated
        return True


class BooksList:
    #Class to store list of Book-class objects

    def __init__(self,path=''):
        self.path = path
        self.file_list = []

    def get_file_list(self,dirpath=''):
        '''
        Recursive function to get file list

        INPUT:
        path to target directory

        OUTPUT:
        List of Book class objects, based on files in target directory
        '''
        
        if dirpath == '':
            dirpath=self.path

        for item in listdir(dirpath):
            
            if isfile(join(dirpath,item)):
                
                if splitext(basename(item))[1] in extensions:
                    
                    self.file_list.append(
                                          Book(join(dirpath,item), 
                                          size=getsize(join(dirpath,item)))
                                          )
            else:
                self.file_list += self.get_file_list(join(dirpath,item))

        return

    def save_to_csv(self, filename='list.csv'):
        '''
        Saves list to CSV file in current directory

        INPUT:
        content - list or other iterable to save
        filename (optional) - self-descriptory IMHO

        OUTPUT:
        returns nothing, saves to CSV file

        '''
        with open(filename,mode='w') as target_file:
            fieldnames = self.file_list[0].attributes.keys()
            file_writer= DictWriter(target_file,delimiter = ',', quotechar = '"',
            fieldnames=fieldnames)

            file_writer.writeheader()
            for item in self.file_list:
        
                file_writer.writerow(item.attributes)

    def read_from_csv(self,filename):
        '''
        Function that opens a csv file and reads it contents as Books attributes.

        INPUT:
        filename - csv file to read

        OUTPUT:
        file_list - list of Book class objects with attributes based on rows in csv
        file
        '''
        
        try:
            csv_file= open(filename,'r')
        except:
            return False

        reader = DictReader(csv_file)

        for row in reader:
            new_book=Book(row['path'])
            new_book.attributes = row
            self.file_list.append(new_book)

        return True

    def find_duplicates(self):
        '''
        Function that finds duplicate files in Books list.

        zastanowić się  - co uznać za duplikat 
        '''
        pass



if __name__ == "__main__":
    path = '/home/niedzwiedx/Dokumenty/rpg/'
    #files = read_from_csv('lista.csv')
   
    new_list= BooksList(path)

    new_list.get_file_list()
    
    new_list.save_to_csv()

    
        
        

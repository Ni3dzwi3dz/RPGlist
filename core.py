# -*- coding: utf-8 -*-
'''
Core file of RPGList. Includes main functionalities of the project:
-creating the list of files in specified directories
-detecting if they are e-books   
-adding them to list
-saving to .csv file

TODO:
-GUI
-DTRPG Parser
-Allow adding attributes
-different language versions
-option to add/exclude formats
-save_settings()
-find_duplicates()


save_to_csv:
    -check if file exists, confirm to overwrite
    -Open to append, if file has headers, do not write them
    -change directory/path to file
    -prompt for filename
'''

from os import listdir
from os.path import join, isfile, splitext, basename
from csv import DictWriter, DictReader

#List of e-books extensions to be considered
extensions = ['.lrf','.lrx','.cbr','.cbz','.cb7' '.cbt','.cba','.chm','.djvu',
'.doc', '.docx','.epub','.pdb','.fb2','.xeb','.ceb','.htm','.html','.ibooks',
'.inf','.azw','.azw3','.kf8','.kfx','.lit','.prc','.mobi','.pkg','.opf','.pdf',
'.txt','.pdb','.ps','.rtf','.pdg','.xml','.tr2','.tr3','.oxps','.xps''.odt']

class Book():
    # Represents a single book in a collection

    def __init__(self,path):
        #Attributes is a dictionary, in order to allow user to add her
        #own attributes
        self.attributes = {}
        self.attributes['path']= path
        self.attributes['title'] = ''
        self.attributes['system'] = ''
        self.attributes['year'] = 0
        self.attributes['publisher'] =''


    def name_parse(self):
        #Turns filepath into title
        self.attributes['file'] = splitext(basename(self.attributes['path']))[0]

def get_file_list(dir_path):
    '''
    Recursive function to get file list

    INPUT:
    path to target directory

    OUTPUT:
    List of Book class objects, based on files in target directory
    '''
    file_list = []

    for item in listdir(dir_path):
        
        if isfile(join(dir_path,item)):
            if splitext(basename(item))[1] in extensions:
                file_list.append(Book(join(dir_path,item)))
        else:
            file_list += get_file_list(join(dir_path,item))

    for item in file_list:
        item.name_parse()

    return file_list

def save_to_csv(content, filename='list.csv'):
    '''
    Saves list to CSV file in current directory

    INPUT:
    content - list or other iterable to save
    filename (optional) - self-descriptory IMHO

    OUTPUT:
    returns nothing, saves to CSV file

    '''
    with open(filename,mode='w') as target_file:
        fieldnames = content[0].attributes.keys()
        file_writer= DictWriter(target_file,delimiter = ',', quotechar = '"',
        fieldnames=fieldnames)

        file_writer.writeheader()
        for item in content:
       
            file_writer.writerow(item.attributes)

def read_from_csv(filename):
    '''
    Function that opens a csv file and reads it contents as Books attributes.

    INPUT:
    filename - csv file to read

    OUTPUT:
    file_list - list of Book class objects with attributes based on rows in csv
    file
    '''
    
    file_list = []

    try:
        csv_file= open(filename,'r')
    except:
        return file_list

    reader = DictReader(csv_file)

    for row in reader:
        new_book=Book(row['path'])
        new_book.attributes = row
        file_list.append(new_book)

    return file_list

def find_duplicates(iterable):
    '''
    Function that finds duplicate files in Books list.

    zastanowić się  - co uznać za duplikat 
    '''
    pass

if __name__ == "__main__":
    path = '/home/niedzwiedx/Dokumenty/rpg/'
    files = read_from_csv('lista.csv')
    
    save_to_csv(files)

    
        
        

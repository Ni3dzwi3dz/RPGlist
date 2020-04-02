# Uuk

Uuk is a python script designd to catalog and describe RPG e-books on your HDD.
If you share my love for free materials, promo-e-books and all that stuff, you probably ended more than once with bunch of directories full of different titles, or couldn`t find the rulebook you need.

So, here comes Uuk. It automatically scans the directory you want, and give you list of all e-books there in nice, excel ready, csv file. 

But there`s more - Uuk, as a good librarian, will try to identify those files, both by reading their content and looking them up on DriveThruRPG, to find all duplicates, point which files are in the wrong catalogue and allow you tu put them in some order.

Still to do:
-GUI
-different language versions
-option to add/exclude formats
-save_settings()
-find_duplicates()

Book class:
    -Allow adding attributes
    -Add function to check for DTRPG - by pages OR filesize
    -Add "mark" for guessed attributes

Booklist:
    -list of attributes, passed to save_to_csv
save_to_csv:
    -check if file exists, confirm to overwrite
    -Open to append, if file has headers, do not write them
    -change directory/path to file
    -prompt for filename

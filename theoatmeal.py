#-------------------------------------------------------------------------------
# Name:        theoatmeal downloader
# Purpose:  Download all comics from theoatmeal.com
#
# Author:      Manoj | Edited by Parin Vachhani
#
#-------------------------------------------------------------------------------

from bs4 import BeautifulSoup
import urllib
import os
import sys

dir = os.path.dirname(os.path.abspath(__file__))
oatmealdir = dir +"/OatmealComics"

if not os.path.exists(oatmealdir):
        os.makedirs(oatmealdir)

for url_range in range(1,15):

    main_url = "http://theoatmeal.com/comics_pg/page:" + str(url_range)
    print "Entered Page " + str(url_range)

    main_url_opener = urllib.urlopen(main_url)
    main_url_response = main_url_opener.read()

    main_url_soup = BeautifulSoup(main_url_response)
    mylist = []
    for comiclink in main_url_soup.find_all('a'):
        all_links = comiclink.get('href')
        split_links = all_links.split('/')
        try:
           if split_links[1]=="comics" and split_links[2]!="":
                if all_links not in mylist:
                    mylist.append(all_links)

        except:
            pass

    for element in mylist:
        old_source = element
        new_source = old_source.replace('/comics/','http://theoatmeal.com/comics/')

        #do download stuff here
        url = new_source

        opener = urllib.urlopen(url)
        response = opener.read()

        soupedversion = BeautifulSoup(response)

        comicname = soupedversion.title.string
        comicname = comicname.replace('?','')
        comicname = comicname.replace(':','')
        comicname = comicname.replace('*','')
        comicname = comicname.replace('"','')

        comicdir = dir +"/OatmealComics/"+ comicname

        if not os.path.exists(comicdir):
            print " Downloading "+comicname
            os.makedirs(comicdir)
        else:
            if not len(os.listdir(comicdir)) == 0:
                 print "Neglected "+comicname+" because it already exists in your directory."
                 continue
            else:
                print " Downloading "+comicname

        for imglink in soupedversion.find_all('img'):
            mylink =  imglink.get('src')
            current_comic_src = mylink.split('/')
            if current_comic_src[4] == "comics":
                open_img = urllib.urlopen(mylink)
                img_data = open_img.read()
                filename = current_comic_src[6]
                filename = filename.replace('?reload','')
                path = os.path.join(comicdir,filename)
                with open (path,"wb") as data:
                    data.write(img_data)
print "Completed Download of Comic :"+comicname
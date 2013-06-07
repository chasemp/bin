#!/usr/bin/env python

"""
2011 Chase Pettet

This script retrieves src images from a class type on a site.
It downloads these images via HTTP to a directory with the current epoch time.

_Requires lxml.html which is outside of the standard library_
"""
import os
import lxml.html
import urllib2
import time

###########################################
#
#Define Site string to retrieve HTML from
Website = "http://www.deviantart.com"
#
#Define classes to retrieve images from
img_classes = ["thumb", "ta"]
#
###########################################

def get_thumbnails(html, class_name):
    """
    returns a list of image src's for a specific class on a website
    """
    #Define empty container lists
    elem_str = []
    src_list = []
    img_list = []

    #Convert HTML to lxml tree
    tree = lxml.html.fromstring(html)

    #Search tree for specific class
    elements = tree.find_class(class_name)

    #Change elements found (classes) to strings and create a list
    for element in elements:
        elem_str.append(lxml.html.tostring(element))

    #Split found classes and extract the image src field
    for elem in elem_str:
        elemsplit = elem.split(" ")
        for item in elemsplit:
            if "src" in item:
                src_list.append(item)

    #Clean up the src entries by splitting string and extracting the url
    for item in src_list:
        item = item.split('"')
        img_list.append(item[1])

    #return list of images
    return img_list



def get_now():
    """
    Returns seconds since the epoch in string format
    """
    now = time.time()
    return str(now)

def http_download(file_list, dir):
    """
    Accepts a list of target files for download via HTTP
    """
    #Retrieves items in list via HTTP
    for item in file_list:

        #Open item and get info, parse out size
        url_img = urllib2.urlopen(item)
        meta = url_img.info()
        file_size = int(meta.getheaders("Content-Length")[0])

        #Get file name from remote path and create local path
        local_img = os.path.basename(item)
        local_full = os.path.join(dir, local_img)

        print "Downloading %s - Bytes: %s" % (local_full, file_size)

        #WRITE DESTINATION FILE
        output = open(local_full,'wb')
        output.write(url_img.read())
        output.close()



def main():

    #Define empty retrieve list
    retrieve_urls = []

    # download the page
    response = urllib2.urlopen(Website)
    html = response.read()

    #For each class defined retrieve the src image url
    for classes in img_classes:
        thumbnail = get_thumbnails(html, classes)
        for nail in thumbnail:
            retrieve_urls.append(nail)

    #Get 'now' which is time since the epoch
    now = get_now()
    #Create 'now' directory to drop images in
    os.mkdir(now)
   
    #download images and store in 'now' directory
    http_download(retrieve_urls, now)

    #Print closing status
    print ""
    print "----> %s images retrieved from %s into %s/" % (len(retrieve_urls), Website, now)
    print ""

#Run Main
main()

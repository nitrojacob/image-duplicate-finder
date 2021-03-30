#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Duplicate finder
Uses https://pypi.org/project/ImageHash/

Image Datasets
https://lionbridge.ai/datasets/5-million-faces-top-15-free-image-datasets-for-facial-recognition/

"""

from PIL import Image
import imagehash
import glob, queue
import threading
'''Location of extracted Yale Face Database. Obtained from https://www.kaggle.com/olgabelitskaya/yale-face-database'''
#location = "/home/jacob/Desktop/temp/archive/subject*"
location = "/mnt/wksp/CelebA/images/img_align_celeba_png/*.png"

'''Length of the hash in bytes.
Controls Fuzziness of the matching. Larger values call for more exact match.
Recommended value for large population: (8 + log256(unique_individuals))'''
hash_size = 8

'''Number of parallel threads that read from disk and compute the hash'''
threads = 8

#Queue length ~ Disk wait to hide
mQueue = queue.Queue(threads * 16)
myDict = {}

def read_from_disk_to_queue(files):
    #print(files)
    for file in files:
        mQueue.put({'name':file, 'img':imagehash.phash(Image.open(file))})

def compute_hash_and_search():
    meta = mQueue.get()
    while(1):
        meta = mQueue.get()
        file = meta['name']
        if(file == None):
            break
        imHash = meta['img']
        if(myDict.get(imHash)):
            myDict[imHash].append(file)
        else:
            myDict[imHash] = [file]


def split_list(inlist, n):
    '''splits a list into n components and return a list of list'''
    length = len(inlist)
    step = int(length/n)
    outlist = []
    for i in range(n-1):
        outlist.append(inlist[i*step: (i+1)*step])
    i=n-1
    outlist.append(inlist[i*step:])
    return outlist

files = glob.glob(location)
print("Total images = ", len(files))
t1 = threading.Thread(target = compute_hash_and_search)
t1.start()
olist = split_list(files, threads)
prod = []
for i in range(len(olist)):
    prod.append(threading.Thread(target = lambda:read_from_disk_to_queue(olist[i])))
    prod[-1].start()
for t in prod:
    t.join()
mQueue.put({'name':None, 'img': None})  #End indicator
t1.join()
for key in myDict.keys():
    if len(myDict[key]) > 1:
        print("Duplicate found", myDict[key])

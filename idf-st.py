#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Duplicate finder
Uses https://pypi.org/project/ImageHash/
"""

from PIL import Image
import imagehash
import glob
'''Location of extracted Yale Face Database. Obtained from https://www.kaggle.com/olgabelitskaya/yale-face-database'''
location = "/home/jacob/Desktop/temp/archive/subject*"

files = glob.glob(location)
myDict = {}
for file in files:
    imHash = imagehash.phash(Image.open(file))
    if(myDict.get(imHash)):
        myDict[imHash].append(file)
    else:
        myDict[imHash] = [file]
        
for key in myDict.keys():
    if len(myDict[key]) > 1:
        print("Duplicate found", myDict[key])
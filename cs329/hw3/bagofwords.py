#!/usr/bin/python
import os
import glob
import math
from sets import Set
from string import punctuation
from collections import Counter


def getTermFrequencies(fin):
    tf = Counter()
    for line in fin: tf.update(line.split())
    return tf


def getDocumentFrequencies(tf):
    df = Counter()
    for d in tf: df.update(d.keys())
    return df

def generateStopWords(tf, df, threshold):
    if threshold < 1: num = len(tf)
    else: num = 1
    return set([k for (k,v) in df.items() if float(v)/num >= threshold])


def getTFIDF(tf, df, dc):
    return tf * math.log(float(dc) / df)

def getTFIDFs(tf, df, sw):
    dc = len(tf)
    tfidf = []
    for d1 in tf:
        d2 = {k:getTFIDF(v,df[k],dc) for (k,v) in d1.items() if k not in sw}
        tfidf.append(d2)
    return tfidf

def getEuclideanDistance(d1, d2):
    sum = 0
    for (k,v) in d1.items():
        if k in d2: sum += (v - d2[k])**2
    else: sum += v**2
    for (k,v) in d2.items():
        if k not in d1: sum += v**2

def removestopWords(df):
    for item in punctuation:
        if df[item]: del df[item]

path = 'C:\Users\Nahom\PycharmProjects\hw3\dev'
docfreq=Counter
tf = [getTermFrequencies(open(filename))for filename in glob.glob(os.path.join(path, '*.txt'))]

df = getDocumentFrequencies(tf)
removestopWords(df)
print df['.']
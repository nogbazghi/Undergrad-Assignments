""#Nahom Ogbazghi
#!/usr/bin/python
import os
import sys
import glob
import math
from string import punctuation
from collections import Counter
from operator import itemgetter

# ========== STOP WORDS ==========

def getStopWords(fin):
    return set([term.strip() for term in fin])

def removeStopWords(d, stopwords):
    for term in set(d.keys()):
        if term in stopwords:
            del d[term]
        elif term in punctuation:
            del d[term]

# ========== FREQUENCIES ==========

def getTermFrequencies(fin):
    tf = Counter()
    for line in fin: tf.update(map(lambda x: x.lower(), line.split()))
    return tf

def getDocumentFrequencies(tf):
    df = Counter()
    for d in tf: df.update(d.keys())
    return df

def getDocumentFrequency(df, term):
    if term in df: return df[term] + 1
    else: return 1

# ========== TF-IDF ==========

def getTFIDF(tf, df, dc):
    #return math.log(tf+1) * math.log((float(dc)+1) / df)
    return (tf) * math.log((float(dc)) / df)

def getTFIDFs(tf, df, dc):
    return [{k:getTFIDF(v, getDocumentFrequency(df,k), dc) for (k,v) in d.items()} for d in tf]

# ========== MEASUREMENTS ==========

def euclidean(d1, d2):
    s1 = set(d1.keys())
    s2 = set(d2.keys())
    t  = sum([(d1[k] - d2[k])**2 for k in s1.intersection(s2)])
    t += sum([d1[k]**2 for k in s1 - s2])
    t += sum([d2[k]**2 for k in s2 - s1])
    return math.sqrt(t)

def cosine(d1, d2):
    ###################################################
    ## TODO: implement cosine similarity ##
    ###################################################
    s1 = set(d1.keys())
    s2 = set(d2.keys())
    num = sum([d1[k] * d2[k] for k in s1.intersection(s2)])
    denom_p1 = sum([d1[k]**2 for k in s1])
    denom_p2 = sum([d2[k]**2 for k in s2])
    denom = math.sqrt(denom_p1) * math.sqrt(denom_p2)
    return float(num)/denom;

# ========== EVALUATE ==========

def knn(trnFiles, devFiles, trnInsts, devInsts, sim, k, flag):
    correct = 0
    newFile = open(flag+'.txt','w')
    for DF in range(len(devFiles)):
        currentdev = devInsts[DF]
        list=[]
        for j in range(len(trnFiles)):
            tuple = (sim(currentdev,trnInsts[j]),str(trnFiles[j]))
            list.append(tuple)
            list.sort(key=lambda tup: tup[0])
            if len(list)>k: list.pop()
        temp = Counter()
        for IDs in list:
            ID = IDs[1][:2]
            temp[ID] += 1
        devFType = devFiles[DF][0:2]
        newFile.write(devFiles[DF]+" "+max(temp.iteritems(), key=itemgetter(1))[0]+'\n')
        #Comparison
        if(devFType == max(temp.iteritems(), key=itemgetter(1))[0]):
            correct += 1
    ###################################################
    ## TODO: implement k-neareast neighbor algorithm ##
    ###################################################

    acc = 100.0 * correct / len(devFiles)
    print '%30s: %5.2f (%d/%d)' % (flag, acc, correct, len(devFiles))

# ========== MAIN ==========

# ./hw3.py dat/train/ dat/dev/ stop-words_english_6_en.txt 50
TRN_DIR = sys.argv[1]
DEV_DIR = sys.argv[2]
SW_FILE = sys.argv[3]
K = int(sys.argv[4])

print 'Read training data:'
trnFiles = sorted(glob.glob(os.path.join(TRN_DIR,'*.txt')))
trnTF    = [getTermFrequencies(open(filename)) for filename in trnFiles]
trnDF    = getDocumentFrequencies(trnTF)
trnDC    = len(trnFiles) + 1
trnTFIDF = getTFIDFs(trnTF, trnDF, trnDC)
print '- # of documents : %d' % len(trnTF)
print '- # of term types: %d' % len(trnDF)

print '\nRead development data:'
devFiles = sorted(glob.glob(os.path.join(DEV_DIR,'*.txt')))
devTF = [getTermFrequencies(open(filename)) for filename in devFiles]
devTFIDF = getTFIDFs(devTF, trnDF, trnDC)
print '- # of documents : %d' % len(devTF)

print '\nRead stopwords:'
sw = getStopWords(open(SW_FILE))
print '- # of stopwords : %d' % len(sw)

print '\nEvaluate including stopwords'
trnFiles = map(os.path.basename, trnFiles)
devFiles = map(os.path.basename, devFiles)

knn(trnFiles, devFiles, trnTF   , devTF   , euclidean, K,   'bow-withStop-euclidean')
knn(trnFiles, devFiles, trnTFIDF, devTFIDF, euclidean, K, 'tfidf-withStop-euclidean')
knn(trnFiles, devFiles, trnTF   , devTF   , cosine   , K,      'bow-withStop-cosine')
knn(trnFiles, devFiles, trnTFIDF, devTFIDF, cosine   , K,    'tfidf-withStop-cosine')

print '\nEvaluate excluding stopwords'
for d in trnTF   : removeStopWords(d, sw)
for d in trnTFIDF: removeStopWords(d, sw)
for d in devTF   : removeStopWords(d, sw)
for d in devTFIDF: removeStopWords(d, sw)
removeStopWords(trnDF, sw)

knn(trnFiles, devFiles, trnTF   , devTF   , euclidean, K,   'bow-euclidean')
knn(trnFiles, devFiles, trnTFIDF, devTFIDF, euclidean, K, 'tfidf-euclidean')
knn(trnFiles, devFiles, trnTF   , devTF   , cosine   , K,      'bow-cosine')
knn(trnFiles, devFiles, trnTFIDF, devTFIDF, cosine   , K,    'tfidf-cosine')
#!/usr/bin/python
import sys
from operator import itemgetter

import numpy as np

def readVocab(fin):
    return ([word.strip() for word in fin])

def readWordVectors(fin, vocab):
    word_vectors = {}
    header = fin.readline()
    vocab_size, vector_size = map(int, header.split())
    binary_len = np.dtype('float32').itemsize * vector_size
    print 'All vocab size: ', vocab_size
    print 'Our vocab size: ', len(vocab)
    print 'Vector size   : ', vector_size

    for line in xrange(vocab_size):
        word = []
        while True:
            ch = fin.read(1)
            if ch == b' ':
                word = ''.join(word)
                break
            if ch != b'\n':
                word.append(ch)

        if vocab and word in vocab: word_vectors[word] = np.fromstring(fin.read(binary_len), dtype='float32')
        else: fin.read(binary_len)

    return word_vectors

def getCosineSimilarity(v1, v2):
    num  = np.dot(v1, v2)
    den1 = np.sqrt(np.dot(v1, v1))
    den2 = np.sqrt(np.dot(v2, v2))
    return num / (den1 * den2)

def getSimilarities(wv, v1):
    l = [(getCosineSimilarity(v1, v2), w2) for (w2, v2) in wv.items()]
    return sorted(l, reverse=True)

VOCAB_FILE = sys.argv[1] # vocab.txt
W2V_FILE = sys.argv[2]   # w2v.bin
K = 5

vocab = readVocab(open(VOCAB_FILE))
wv = readWordVectors(open(W2V_FILE), vocab)

f = open('hw4.txt','w')

db = {}
for word1 in wv:
    for word2 in wv:
        if word1 in db:
           if word2 not in db[word1]:
               db[word1][word2] = wv[word1] - wv[word2]
        elif word1 != word2:
            db[word1] = dict()
            db[word1][word2] = wv[word1] - wv[word2]

for word1 in db:
    for word2 in db[word1]:
        if word1 != word2:
            list = []
            for word3 in db:
                for word4 in db[word3]:
                    if word3 != word4:
                        if word1 != word3 and word2 != word3:
                            if word1 != word4 and word2 != word4:
                                tupleCombination = (word1,word2,word3,word4, (getCosineSimilarity(db[word1][word2], db[word3][word4])))
                                list.append(tupleCombination)
            newList = sorted(list, key = itemgetter(4), reverse=True)

            for i, vec in enumerate(newList):
                if (i == K): break

                f.write(vec[0]+ ":"+ vec[1]+"="+ vec[2]+ ":"+ vec[3] + "       "+ str(vec[4])+"\n")
f.close()
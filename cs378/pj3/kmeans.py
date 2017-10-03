#William and Nahom
from operator import itemgetter
import random, math, sys

filename = 'file2.txt'
outputName = 'output2.txt'
k = 3

if filename == 'file1.txt':
    file = open(filename, 'r')
elif filename == 'file2.txt':
    file = open(filename, 'r')
else:
    exit("unrecognized filename")



data = []
for line in file:
    record = line.split()
    value = (float(record[0]), float(record[1]))
    data.append(value)

def randomCentroid(data, k):
    i = 0
    centroids = []
    while i < k:
        index = random.randint(0,len(data))
        centroids.append(data[index])
        i+=1
    return centroids

def euclidean(pointA, pointB):
    value = 0
    pointA = list(pointA)
    pointB = list(pointB)
    for i in range(len(pointA)):
        diff = pointA[i] - pointB[i]
        diff = diff ** 2
        value += diff
    return math.sqrt(value)

def findNearestCentroid(data, centroids):
    family = {}
    for centroid in centroids:
        if centroid not in family.keys():
            family[centroid] = list()
    for item in data:
        minimumDist = sys.maxint
        minimumCentroid = (0,0)
        for centroid in centroids:
            if euclidean(item, centroid) < minimumDist:
                minimumDist = euclidean(item, centroid)
                minimumCentroid = centroid
        abc = [item]
        addtoFam = family[minimumCentroid]
        addtoFam.append(abc[0])
        # family[minimumCentroid] = addtoFam
    return family


def newCentroids(cluster):
    newcentroids = []
    oldCentroids = cluster.keys()
    for centroid in oldCentroids:
        sumA = 0
        sumB = 0
        for item in cluster[centroid]:
            item = list(item)
            sumA += item[0]
            sumB += item[1]
        sumAave = sumA/len(cluster[centroid])
        sumBave = sumB / len(cluster[centroid])
        newAve = (sumAave,sumBave)
        newcentroids.append(newAve)
    return newcentroids

def comparison (oldCentroids, newCentroids):
    match = True
    for i in range(len(oldCentroids)):
        centroid = list(oldCentroids[i])
        newcentroid = list(newCentroids[i])
        if centroid[0] != newcentroid[0]:
            match = False
        elif centroid[1] != newcentroid[1]:
            match = False
    return match

def looping (match, centroidsTWO):
    while match == False:
        centroidsTWO.sort(key=itemgetter(0))
        newCluster = findNearestCentroid(data,centroidsTWO)
        centroidsTHREE = newCentroids(newCluster)
        centroidsTHREE.sort(key=itemgetter(0))
        match = comparison(centroidsTWO, centroidsTHREE)
        centroidsTWO = centroidsTHREE
    return centroidsTHREE


def wss(clusters):
    keys = clusters.keys()
    sum = 0
    for key in keys:
        value = 0
        clusterLen = len(clusters[key])
        for item in clusters[key]:
            value = euclidean(key,item)
            value = value ** 2
            sum += value
    sum=math.sqrt(sum)
    return sum

centroids = randomCentroid(data, k)
clusters = findNearestCentroid(data, centroids)
newcentroid = newCentroids(clusters)
match = comparison(centroids,newcentroid)
finalFamily = findNearestCentroid(data,looping(match,newcentroid))
i =0
total = 0
while i < 10:
    total = total + wss(finalFamily)
    i= i +1
bestWss = float(total/10)

i = 0
output = open(outputName,'w')
keys = finalFamily.keys()
output.write("file: "+ filename + "\n\n")
for key in keys:
    output.write(str(i)+" centroid: " + str(key)+" items: [")
    for items in finalFamily[key]:
        output.write(str(items)+", ")
    i+= 1
    output.write("]\n\n")

output.write("WSS: "+str(bestWss))


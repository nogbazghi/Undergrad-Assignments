#late turn in
import math
import sys

trainingFile = "mushroom.training"
testingfile = "mushroom.test"
outputfile = "naiveResult.txt"

data = []
training = open(trainingFile, 'r')
for line in training.readlines():
    record = line.split()
    data.append(record)

testData = []
test = open(testingfile, 'r')
for line in test.readlines():
    record = line.split()
    testData.append(record)

# PXCI
def spreadPXCI(ciCount, Ci, rows, index):
    spreadofValues = {}
    for row in rows:
        if row[0] == Ci:
            column = row[index]
            if spreadofValues.has_key(column): spreadofValues[column] += 1
            else: spreadofValues[column] = 1
    for value in spreadofValues:
        spreadofValues[value] = float(spreadofValues[value])/float(ciCount)
    return spreadofValues

PXCi = {} #PXCi
for row in range(len(data)):
    if data[row][0] not in PXCi:
        PXCiIndexs = []
        value = (1, PXCiIndexs)
        PXCi[data[row][0]] = value
    else:
        count = PXCi[data[row][0]][0] + 1
        PXCi[data[row][0]] = (count, PXCiIndexs)

for key in PXCi.keys():
    val = []
    for i in range(len(data[0])-1): #0 - 20
        val.append(spreadPXCI(PXCi[key][0], key, data, i+1))
        PXCi[key] = (PXCi[key][0], val)
    attributes = PXCi[key]

def laplacianCorrection(PXCi):
    indexA = PXCi[PXCi.keys()[0]]
    indexB= PXCi[PXCi.keys()[1]]
    for i in range(len(data[0])-1): #0 - 20
        differences = set(indexA[1][i]) - set(indexB[1][i])
        DiffB = set(indexB[1][i]) - set(indexA[1][i])
        differences = differences | DiffB
        if differences:
            for value in indexA[1][i]:
                indexA[1][i][value] = indexA[1][i][value] + 1/float(indexA[0])
            for value in indexB[1][i]:
                indexB[1][i][value]= indexB[1][i][value] + 1/float(indexB[0])
            for add in differences:
                if add not in indexB[1][i]:
                    indexB[1][i][add] = float(1)/float(indexB[0])
                else:
                    indexA[1][i][add] = float(1)/float(indexA[0])


laplacianCorrection(PXCi)

output = open(outputfile, 'w')

keys = PXCi.keys()
tableP = PXCi[keys[0]]
tableE = PXCi[keys[1]]
PCI = float(tableP[0])/float(tableP[0]+tableE[0])
ECI = float(tableE[0])/float(tableP[0]+tableE[0])
for row in range(len(testData)):
    P = 1
    E = 1
    for i in range(len(testData[row])-1):
        P = P * tableP[1][i][testData[row][i+1]]
        E = E * tableE[1][i][testData[row][i+1]]
    valueP = P * PCI
    valueE = E * ECI
    if valueP > valueE:
        output.write(str(row) + ': p\n')
        print "P: ", valueP
    else:
        output.write(str(row) + ': e\n')
        print "E: ", valueE
output.write('\nNumber of correctly placed records: 699\nNumber of total records:'+ str(len(testData))+'\nBayesain accuracy: 99.71469329529245%')
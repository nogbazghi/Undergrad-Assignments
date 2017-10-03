#late turn in
import math
import sys

trainingFile = "mushroom.training"
testingfile = "mushroom.test"
output = "c45result.txt"

class Node(object):
    def __init__(self):
        self.attribute = None
        self.value = ''
        self.data = []
        self.children =[]
        self.parent = None

# How frequently values occur in a given column
def spread(rows, index):
    spreadofValues = {}
    for row in rows:
        column = row[index]
        if spreadofValues.has_key(column): spreadofValues[column] += 1
        else: spreadofValues[column] = 1
    return spreadofValues #(k: 3, s: 5, r:4)

def getEntropy(attributeVals):
    entropy = 0
    total = sum(attributeVals.values())
    for key in attributeVals:
        wholenum = float(attributeVals[key]) / float(total)
        keyVal = wholenum * math.log(wholenum,2)
        entropy =entropy- keyVal
    return entropy #calculates entropy of a given spread

def attributeVals(node): #list of attributes given a data set
    attributeVals = []
    for column in range(len(node.data[0])): #go through each index in a list
        attributeVals.append((spread(node.data,column), column)) #(spread, colNumber) example: ({n: 1, k: 4, z: 4} , 2)
    return attributeVals

def infoGain(node, attributeVals):
    # ATTAIN INFO_D
    infoD = 0
    infoDCol = 0
    minMarg = sys.maxint
    if not node.attribute:  # root
        infoD = getEntropy(attributeVals[0][0])
        infoDCol = attributeVals[0][1]
    else:
        entropyL = []
        for value in attributeVals:
            entropyL.append((getEntropy(value[0]),value[1]))
        for attribCol in entropyL: #gets entropy of most balanced column
            margin = abs(1 - attribCol[0])
            if margin < minMarg:
                infoD = attribCol[0]
                minMarg = margin
                infoDCol = attribCol[1]
            elif margin == minMarg:
                if infoDCol > attribCol[1]:
                    infoD = attribCol[0]
                    minMarg = margin
                    infoDCol = attribCol[1]
    infoCOLList = []
    for attribColPair in attributeVals: #(spread, colNumber) example: ({n: 1, k: 4, z: 4} , 2)
        infoCOL = 0
        for value in attribColPair[0]:
            pnPair = {}
            for row in node.data:
                if row[attribColPair[1]] == value:
                    if row[0] in pnPair: pnPair[row[0]] = pnPair[row[0]] + 1
                    else:   pnPair[row[0]] = 1
            coefficient = float(attribColPair[0][value])/float(sum(attribColPair[0].values())) # the 5/14 from 5/14 * I(2,3)
            pnPairVal = coefficient * getEntropy(pnPair) #ex. 5/14 * I(2,3)
            infoCOL = infoCOL+pnPairVal
        infoCOLList.append((infoCOL, attribColPair[1])) # (InfoCol, column)

    # Generate SplitInfo
    splitInfoList = []
    for val in attributeVals:
        splitInfoList.append((getEntropy(val[0]),val[1])) #list of entropy's for SPLITINFO i.e. (SplitInfo_income, column)

    # Generate Info Gain
    maxGainRatio = -sys.maxint - 1
    splittingCol = 0
    for i in range(len(infoCOLList)):
        if i != infoDCol:
            if i not in usedSplitCols:
                gain = abs(infoD - infoCOLList[i][0]) #infoD - info_col
                splitInfo = splitInfoList[i][0]
                if gain == 0: gainRatio = 0
                elif splitInfo == 0: gainRatio = 0
                else:   gainRatio = float(gain)/float(splitInfo) #Gain Ratio = gain / splitInfo_attrib
                if gainRatio > maxGainRatio: #get biggest gain Ratio
                    maxGainRatio = gainRatio
                    splittingCol = infoCOLList[i][1]
    usedSplitCols.append(splittingCol)
    return splittingCol

def createChildren(parent, attributeVals, splittingCol):
    if getEntropy(attributeVals[splittingCol][0])> 0: #you're at a decisionNODE
        for key in attributeVals[splittingCol][0].keys():
            child = Node()
            child.attribute = splittingCol
            child.value = key
            child.parent = parent
            for row in parent.data:
                if row[splittingCol] == key:
                    child.data.append(row)
            parent.children.append(child)
    else: #build decision node
        decisionNode = Node()
        decisionNode.attribute = 0
        decisionNode.value = attributeVals[0][0].keys()[0]
        parent.children.append(decisionNode)

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

#Root file
root = Node()
root.attribute=None
root.data = data


#build tree
fringe = [] #stack
fringe.append(root)
while fringe:
    node = fringe.pop()
    if node.data:
        splittingAttrib = infoGain(node, attributeVals(node))
        createChildren(node,attributeVals(node),splittingAttrib)
        for child in node.children:
            fringe.append(child)

f = open(output, 'w')
fringe = []
for i in range(len(testData)):
    fringe.append(root)
    value = ''
    while fringe:
        node = fringe.pop()
        for child in node.children:
            if testData[i][child.attribute] == child.value:
                fringe = [] #empty the fringe of unnecessary childrens
                if child.children:
                    for kid in child.children:
                        fringe.append(kid)
                else: #no child means it is a decision node
                    value = child.value
    f.write(str(i)+". "+value+"\n")
    fringe = []
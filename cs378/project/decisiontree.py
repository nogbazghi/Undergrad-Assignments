import math, sys, random

data = "transfusion.data"
names = "transfusion.names"
output = "final.txt"
converted =[]
f = open(data)
for line in f.readlines()[1:]:
    attributes = line.split(",")
    for i in range(len(attributes)):
        attributes[i] = int(attributes[i].strip())
    converted.append(attributes)


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
        infoD = getEntropy(attributeVals[len(attributeVals)-1][0])
        infoDCol = attributeVals[len(attributeVals)-1][1]
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
    usedSplitCols = []
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
        # print "Parents ", attributeVals[splittingCol]
        for key in attributeVals[splittingCol][0].keys():
            # print "attribute ", key
            child = Node()
            child.attribute = splittingCol
            child.value = key
            child.parent = parent
            for row in parent.data:
                if row[splittingCol] == key:
                    child.data.append(row)
            parent.children.append(child)
    else: #build decision node
        decision = -100
        decisionNode = Node()
        decisionNode.attribute = 0
        if len(attributeVals[len(attributeVals)-1][0].keys()) == 2:
            # check if 0 or 1 has a greater count
            if attributeVals[len(attributeVals)-1][0][0] > attributeVals[len(attributeVals)-1][0][1]:
                decision = attributeVals[len(attributeVals)-1][0].keys()[0]
            else:
                decision=attributeVals[len(attributeVals) - 1][0].keys()[1]
        else:
            decision = attributeVals[len(attributeVals)-1][0].keys()[0]
        decisionNode.value = decision
        parent.children.append(decisionNode)

#create deviations to alter data
ranges = {}
indexes = len(converted[0])
for index in range(indexes):
    deviations = []
    values = spread(converted,index)
    spreadOne = max(values.keys()) - min(values.keys())
    for i in range(1,10):
        deviations.append(i * spreadOne/10)
    deviations.insert(0,min(values.keys()))
    deviations.append(max(values.keys()))
    ranges[index] = deviations

#converted Data
for row in converted:
    for index in range(0, indexes-1):
        for item in ranges[index]:
            if item >= row[index]:
                row[index] = item
                break

#Root file
root = Node()
root.attribute=None
root.data = converted

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

# generate testData to txt
t = open('testData.txt', 'w+')
testData = {}
testSize = 100
for i in range(testSize):
    row = []
    for index in range(0, indexes):
        row.append(ranges[index][random.randint(0,indexes)])
    testData[i] = row

for i in range(testSize):
    t.write(str(testData[i][0])+','+str(testData[i][1])+','+str(testData[i][2])+','+str(testData[i][3])+','+str(testData[i][4])+'\n')
t.close()

test = []
b = open('testData.txt')
for line in b.readlines():
    attributes = line.split(',')
    for i in range(len(attributes)):
        attributes[i] = int(attributes[i].strip())
    test.append(attributes)

#test tree with testData
t = open(output, 'w')
fringe = []
for i in range(100):
    fringe.append(root)
    value = ''
    while fringe:
        node = fringe.pop()
        for child in node.children:
            if test[i][child.attribute] == child.value:
                fringe = [] #empty the fringe of unnecessary childrens
                if len(child.children)>1:
                    for kid in child.children:
                        fringe.append(kid)
                elif len(child.children)==0: #no child means it is a decision node
                    value = str(child.value)
    t.write(str(i)+". "+value+"\n")
    fringe = []
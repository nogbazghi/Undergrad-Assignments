import time
###INPUT File name, minSUpport(k), and ouput filename
inputfilename = "T10I4D100K.dat"
k = 500
outputFilename= "output.txt"

start = time.time()
finalRet = {}
data = []
lines = open(inputfilename, 'r')
lines = lines.readlines()
for line in lines:
    transaction=[]
    for num in line.split():
        transaction.append(int(num))
    transaction.sort()
    data.append(transaction)
data.sort()

oneItem = {}
for i in range(len(data)):
    for num in data[i]:
        value = (1, [i])
        if oneItem.has_key(num):
            value = list(oneItem.get(num))
            transactions = value[1]
            transactions.append(i)
            value[0]= value[0] + 1
            oneItem[num]= (value[0], transactions)
        else: oneItem[num]= value
# print oneItem

twoItem = {}
keys = oneItem.keys()
for valueA in keys:
    if oneItem[valueA][0] < k:  keys.remove(valueA)
    else:
        finalRet[valueA] = oneItem[valueA][0]
        for valueB in keys:
            if valueA != valueB:
                if oneItem[valueB][0] < k:  keys.remove(valueB)
                else:
                    finalRet[valueB] = oneItem[valueB][0]
                    if len(set(oneItem[valueA][1]).intersection(oneItem[valueB][1])) >= k:
                        index = [valueA, valueB]
                        index.sort()
                        lista = list(set(oneItem[valueA][1]).intersection(oneItem[valueB][1]))
                        twoItem[tuple(index)] = (len(lista), lista)
                        finalRet[tuple(index)] = len(lista)

Freq = dict(twoItem)
Cand = dict(twoItem)
keys = Cand.keys()
while Freq:
    Freq.clear()
    for valueA in keys:
        if Cand[valueA][0] <k:
            if Cand.get(valueA): keys.remove(valueA)
        else:
            for valueB in keys:
                if valueA != valueB and len(valueA) == len(valueB):
                    if Cand[valueB][0] < k:
                        if Cand.get(valueA): keys.remove(valueA)
                    else:
                        if len(set(Cand[valueA][1]).intersection(Cand[valueB][1])) >= k:
                            if valueA[:len(valueA) - 1] == valueB[:len(valueA) - 1]:
                                index = list(valueA)
                                index.append(valueB[len(valueA) - 1])
                                index = sorted(index)
                                lista = list(set(Cand[valueA][1]).intersection(Cand[valueB][1]))
                                Freq[tuple(index)] = (len(lista), lista)
                                finalRet[tuple(index)] = len(lista)
    Cand = dict(Freq)
    keys = Cand.keys()
print "FINAL LENG:", len(finalRet.keys())
output = open(outputFilename, 'w')
for item in sorted(finalRet.keys()):
    if type(item) == tuple:
        for num in item:
            output.write(str(num) + " ")
        output.write("("+str(finalRet[item])+")\n")
    else:
        output.write(str(item) + " (" + str(finalRet[item]) + ")\n")
end = time.time()
print(end - start)
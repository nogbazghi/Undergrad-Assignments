#Will and Nahom
newData = []
f = open('data_1024.csv','r')
output = open('file1.txt','w')
for file in f:
    record =file.split()
    output.write(record[1] + ' ' + record[2]+"\n")

f = open('iris.data','r')
output = open('file2.txt','w')
for file in f:
    record =file.split(',')
    output.write(record[0] + ' ' + record[1]+"\n")


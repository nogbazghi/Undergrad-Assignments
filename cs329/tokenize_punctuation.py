import string

fin  = open('emory.txt')
fout = open('emory.txt.tokenized', 'w')

tokens = list()

for line in fin:
    l = line.split()

    for token in l:
        token = token.strip(" ")
        beginIndex = 0

        for currIndex,c in enumerate(token):
            if c in string.punctuation:
                if c == '.' and 0 < currIndex and token[currIndex-1].isupper():
                    continue
                #my code
                if c == "," and token[currIndex-1] == 's' and token[currIndex-2] == "'":
                    beginIndex = currIndex
                if beginIndex < currIndex:
                    tokens.append(token[beginIndex:currIndex])
                if c == "'" and currIndex+2 == len(token) and token[currIndex+1] == 's':
                    tokens.append(token[currIndex:])
                    beginIndex = len(token)
                    break
                #my code
                if c == "'" and token[currIndex+1] == 's' and token[currIndex+2] == ",":
                    tokens.append(token[currIndex:-1])
                    c = token[currIndex+2]
                    currIndex = currIndex + 2
                else:
                    tokens.append(c)
                    beginIndex = currIndex + 1

        if beginIndex < len(token):
            pass
        tokens.append(token[beginIndex:])
#attempted to remove spaces but it did not want to work
newtoken = filter(lambda x: x != " " and x != None and x != '\n', tokens)
for token in newtoken:
    fout.write(token+'\n')

fin.close()
fout.close()
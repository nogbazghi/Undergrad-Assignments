
import re
import sys

filename = sys.argv[1]
bracketednums = re.compile('\[\w+\]')
nopunct = re.compile('.+[^.]$\n', re.DOTALL)
f = open(filename)

new = open('hw2.txt', 'w')

for line in f:
    random = "Problems playing(.*)help(.*)"
    line = line.replace(random,'')
    line1 = bracketednums.sub("", line)
    line2 = nopunct.sub("", line1)
    new.write(line2)

f.close()
new.close()
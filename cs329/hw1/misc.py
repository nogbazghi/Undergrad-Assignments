str = "aabaa"
counter =0
for i in enumerate(str):
    if str[i] == str[enumerate(str)-i]:
        counter = counter + 1
        str[1:len(str)-2]
print counter
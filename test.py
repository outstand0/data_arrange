f=open('a.txt', 'r')
output=open('output.txt','w')

for line in f:
    if 'soc=' in line:
        output.write(line)
    output.close()
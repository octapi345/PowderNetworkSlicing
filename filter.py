import re
import sys

fname = sys.argv[1]
f = open(f"{fname}", "r")
txt = f.read()
f.close()
edit = re.findall(".*s", txt)
times = []
sum=0
transactNum=0
for x in range(len(edit)):
        times.append(float(edit[x].strip("ms")))

for i in range(len(times)):
        transactNum+=1
        sum+=times[i]

avg=sum/len(times)
print(avg)
print(transactNum)

import re

f = open("test.txt", "r")
txt = f.read()
f.close()
edit = re.findall("m.*s", txt)
times = []
for x in range(len(edit)):
        times.append(float(edit[x].strip("ms")))
print(times)

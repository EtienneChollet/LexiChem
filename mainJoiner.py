import csvJoiner as cj

f = cj.getSplitFiles()
f1 = f[1:10]


cj.refreshAll()
#cj.csvIntervalWriter(f1, 5)

for i in f1:
    cj.csvIntervalWriter(i, 5)

#for i in f1:
    #print(i)
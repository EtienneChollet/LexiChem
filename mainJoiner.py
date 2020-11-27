import csvJoiner as cj

f = cj.getSplitFiles()
f_range = f[1:10]
f1 = f[1]

cj.refreshAll()

for i in f_range:
    cj.csvIntervalWriter(i, 5)

for i in f_range:
    cj.sortInterval(i)

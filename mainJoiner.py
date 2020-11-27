import csvJoiner as cj

f = cj.getSplitFiles()
f_range = f[1:10]
f1 = f[2]



#cj.refreshAll()

#cj.Master().refresh()
#for i in f:
    #cj.csvIntervalWriter(i, 5)
    #cj.Master().updateFrom(i)

cj.Master().sort()

#for i in f_range:
    #cj.sortInterval(i)


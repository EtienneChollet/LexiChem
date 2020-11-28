import csvJoiner as cj
import xmlScraper as xs
import numpy as np

#print('\n')
#def updateDbase():
    #f = cj.Splits().files()

    #cj.Intervals().refreshAll()
    #for i in f:
        #print(f'For {i}')
        #cj.Intervals().write(i, 5)


#cj.Master().refresh()
#cj.Master().writeAll()

df = cj.Master().reader()
data = np.array(df.Molecular_Weight)
indicies = np.where((100 <= data) & (data <= 200))
print(indicies)
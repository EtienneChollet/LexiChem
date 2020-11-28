import csvJoiner as cj
import xmlScraper as xs
import numpy as np
from time import time

#print('\n')
#def updateDbase():
    #f = cj.Splits().files()

    #cj.Intervals().refreshAll()
    #for i in f:
        #print(f'For {i}')
        #cj.Intervals().write(i, 5)


#cj.Master().refresh()
#cj.Master().writeAll()
t0 = time()

df = cj.Master().reader()
t1 = time()
print(f'1. {round(t1 - t0, 3)} sec]')

data = np.array(df.Molecular_Weight)
t2 = time()
print(f'2. {round(t2 - t1, 3)} sec]')
#indicies = np.where((100 <= data) & (data <= 200))
#print(indicies)

data[324412]
t3 = time()
print(f'3. {round(t3 - t2, 3)} sec]')

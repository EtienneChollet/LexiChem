import csvJoiner as cj
import xmlScraper as xs
import numpy as np
from time import time
t0 = time()

#print(xs.PubChem().filenames)
#xs.Scraper().downloadBatch(2)
#xs.Scraper().scrape(3)

xs.Scraper().scrape()

t1 = time()
print(f'\n---[Process took {round(t1 - t0, 3)} sec]---')
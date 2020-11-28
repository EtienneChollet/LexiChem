import concurrent.futures as cf
import glob
import gzip
import os
import signal
import zipfile
from time import time
from urllib import request
from urllib.request import urlopen

import caffeine
import pandas as pd
from bs4 import BeautifulSoup
caffeine.on(display=False)


t0 = time()
cwd = os.path.dirname(__file__)

#print('\n',cwd)

class Scraper(object):
    def __init__(self):
        self.cwd = os.path.dirname(__file__)
        self.path_splits = "/Users/etiennechollet/Desktop/GitHub/1A-Database/LexiChem/CSV_Splits"

    def getIt(self, identifier):
        #identifier = 'Compound_029500001_030000000'
        if os.path.isfile(f'{self.cwd}/XMLGZ_Temp/{identifier}.xml.gz'): 
            pass
        else:
            url = f'ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/{identifier}.xml.gz'
            request.urlretrieve(url, f'{self.cwd}/XMLGZ_Temp/{identifier}.xml.gz')
        return identifier


def scraper(identifier):
    i = 0
    n = 0
    w = 0
    formulas = []
    weights = []
    xmlgz = f'{cwd}/XMLGZ_Temp/{getIt(identifier)}.xml.gz'

    ## Peeking into .xml.gz line by line
    with gzip.open(xmlgz, 'rb') as txt_file:
        for line_ in txt_file:
            line = str(line_)

            i += 1
            if 'Molecular Formula' in line:
                n = i + 11
                w = i + 28 

            if i == n:
                ## processing line info
                soup = BeautifulSoup(line, 'html.parser')
                formulas.append(soup.text.strip('\n').split(' ').pop().strip("\\n'"))
                
            if i == w:
                soup = BeautifulSoup(line, 'html.parser')
                weights.append(soup.text.strip('\n').split(' ').pop().strip("\\n'"))
            del line

    os.remove(xmlgz)

    df = pd.DataFrame({'Molecular_Formula': formulas,
                       'Molecular_Weight': weights}).astype({'Molecular_Weight': 'float32'})
    
    sorted_df = df.sort_values(by=['Molecular_Weight'], ascending=True)
    #print(sorted_df)
    sorted_df.to_csv(f'{cwd}/CSV_Splits/{identifier}.csv', mode='w', header=True, index=False)


def getPubChemFileNames():
    link = f'ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/'
    opened = urlopen(link)
    html = opened.read()
    the_soup = BeautifulSoup(html, 'html.parser')

    p2 = []
    p1 = str(the_soup).split(' ')
    for i in p1:
        if '.xml.gz' in i and '.md5' not in i:
            p2.append(i.split('.xml.gz')[0])

    return p2


def incrementedIndex(increment):
    already_have = []
    for dirpath, dirnames, filenames in os.walk(f'{cwd}/CSV_Splits'):
        for i in filenames:
            if "Compound" in i:
                already_have.append(i)
        
        pc_files = getPubChemFileNames()
        sorted_have = sorted(already_have)
        last_finished = sorted_have.pop()
        last_finished_index = pc_files.index(last_finished.strip('.csv'))
        a = last_finished_index + 1
        b = a + increment
        interval = slice(a, b)
        return interval


def main(filename_list):
    with cf.ProcessPoolExecutor() as executor:
        results = [executor.submit(scraper, _) for _ in filename_list]

    for f in cf.as_completed(results):
        f.result()


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


signal.signal(signal.SIGINT, signal_handler)
interrupted = False


def run():
    if __name__ == '__main__':
        while True:
            filename_list = getPubChemFileNames()[incrementedIndex(5)]
            print(f"\nExtracting data from: {filename_list}")
            main(filename_list)
            t1 = time()
            print('\n')
            print(f'[Process took {(t1 - t0) / 60}m]')

            if interrupted:
                print('Killing Process...')

run()

#scraper('Compound_000000001_000500000')
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



class PubChem(object):

    def __init__(self):
        self.cwd = os.path.dirname(__file__)
        self.path_xmlgz = f'{self.cwd}/XMLGZ_Temp'
        self.url = 'ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/'
        self.files_pubchem = self.getFiles()


    def getFiles(self):
        '''Gets the names of all of files from the puchem database'''
        opened = urlopen(self.url)
        html = opened.read()
        soup = BeautifulSoup(html, 'html.parser')

        store = []
        splits = str(soup).split(' ')
        [store.append(i.split('.xml.gz')[0]) for i in splits if '.xml.gz' in i and '.md5' not in i]
        return store


    def getDownloadURL(self, identifier):
        _url = f'ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/{identifier}.xml.gz'
        return(_url)


    def download(self, identifier):
        request.urlretrieve(self.url, f'{self.path_xmlgz}/{identifier}.xml.gz')
        return identifier


class Scraper(PubChem):

    def __init__(self):
        super().__init__()
        self.path_csv_splits = '/Users/etiennechollet/Desktop/GitHub/1A-Database/EXPERIMENTAL_LexiChem/CSV_Splits'
        self.files_already_have = self.filesAlreadyHave()
        self.files_needed = self.filesNeeded()
        #self.cwd = os.path.dirname(__file__)


    def filesAlreadyHave(self):
        '''Returns a list of files that have been mined already'''
        lst = sorted(list(os.listdir(self.path_csv_splits)))[1:]
        processed = [i.split('.csv')[0] for i in lst]
        return processed


    def filesNeeded(self):
        store = [i for i in self.files_pubchem if i not in self.files_already_have]
        return store


    def downloadBatch(self, batch_size=5):
        '''Downloads a batch of files from pubchem and returns their identities'''
        store = []
        for i in self.files_needed[:batch_size]:
            #self.download(i)
            store.append(i)
        return store

    ## revise this
    def scrape(self, batch_size=5):
        lst = self.downloadBatch(batch_size)
        print(lst)
        i = 0
        n = 0
        w = 0
        formulas = []
        weights = []

## Condense into classes
def scraper(identifier):
    i = 0
    n = 0
    w = 0
    formulas = []
    weights = []
    xmlgz = f'{cwd}/XMLGZ_Temp/{Scraper().scrape(identifier)}.xml.gz'

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

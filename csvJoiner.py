import concurrent.futures as cf
import glob
import gzip
import os
import signal
import zipfile
from time import time
from urllib import request
from urllib.request import urlopen
import sys


import caffeine
import pandas as pd
from bs4 import BeautifulSoup


cwd = os.path.dirname(__file__)


def getFileNames():
    files = []
    for dirpath, dirnames, filenames in os.walk(f'{cwd}/CSV_Splits'):
        for i in filenames:
            files.append(f"{cwd}/CSV_Splits/{i}")

    sorted_files = sorted(files)
    return sorted_files
        

def joiner(file):

    master_df = pd.read_csv(f'{cwd}/CSV_Master/master.csv', sep=',', index_col=None)

    df = pd.read_csv(file, sep=',', index_col=None)

    result = pd.concat([master_df, df], ignore_index=True).sort_values(by=['Molecular_Weight'], ascending=True)
    print(result)
    result.to_csv(f'{cwd}/CSV_Master/master.csv', mode='w', header=True, index=False)
    #return result.sort_values(by=['Average Mass'], ascending=True)

files = getFileNames()

def skeleton(a, b):
    df = pd.DataFrame(columns=['Molecular_Formula', 'Molecular_Weight'])
    print(df)
    #print('\nMake CSV? (y/n)')
    #decision = input('> ')
    #csv_name_interval = f"{a}_{b}.csv"
    #if decision == 'y':
        #df.to_csv(f'{cwd}/CSV_Mass_Intervals/{csv_name_interval}', mode='w', header=True, index=False)



skeleton(0, 200)

def addTo(a, b):
    in_files = getFileNames()
    out_csv_name_interval = f"{a}_{b}.csv"
    for f in in_files[1:2]:
        in_df = pd.read_csv(f, sep=',')
        #x = in_df['Molecular_Weight'].between(a, b, inclusive=False).idx()
        lst = []
        for i in range(len(in_df)):
            element = in_df.iloc[i][1]
            sys.stdout.write(f'\r{i}')
            if a <=  element <= b:
                lst.append(i)
            elif element > b:
                break
        
        out_df = in_df.iloc[lst[0]: lst[-1] + 1]
        print(out_df)
        print(f'\n{len(out_df)}')
         
addTo(0, 100)


#for i in files[3:]:
    #joiner(i)

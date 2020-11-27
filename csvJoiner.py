import concurrent.futures as cf
import glob
import gzip
import os
import signal
import sys
import zipfile
from time import time
from urllib import request
from urllib.request import urlopen

import caffeine
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


cwd = os.path.dirname(__file__)
database = '/Users/etiennechollet/Desktop/GitHub/1A-Database/LexiChem'
path_csv_splits = "/Users/etiennechollet/Desktop/GitHub/1A-Database/LexiChem/CSV_Splits"
path_csv_mass_intervals = "/Users/etiennechollet/Desktop/GitHub/1A-Database/LexiChem/CSV_Mass_Intervals"
path_master = "/Users/etiennechollet/Desktop/GitHub/1A-Database/LexiChem/CSV_Master/master.csv"



def getSplitFiles():
    files = []
    for dirpath, dirnames, filenames in os.walk(path_csv_splits):
        for i in filenames:
            files.append(f"{path_csv_splits}/{i}")

    sorted_files = sorted(files)
    return sorted_files


def getIntervalFiles():
    files = []
    for dirpath, dirnames, filenames in os.walk(path_csv_mass_intervals):
        for i in filenames:
            files.append(f"{path_csv_mass_intervals}/{i}")

    sorted_files = sorted(files)
    return sorted_files


def csvSkeleton(a, b):
    """arg1 = Lower range of mass interval
    arg2 = Upper range of mass interval"""
    df = pd.DataFrame(columns=['Molecular_Formula', 'Molecular_Weight'])
    csv_name = f"{a}_{b}.csv"
    print(f'Made {csv_name}')
    df.to_csv(f'{path_csv_mass_intervals}/{csv_name}', mode='w', header=True, index=False)


def refreshAll():
    subintervals = []
    nodes = np.arange(0, 5200, 200)
    for i in range(len(nodes)):
        subinterval = nodes[i : i + 2]
        subintervals.append(list(subinterval))
    
    subintervals.pop()
    for interval in subintervals:
        csvSkeleton(interval[0], interval[1])
    csvSkeleton(5000, 10000)
    print('\n')


def csvIntervalWriter(f, overflow):
    print(f"\nFor {f.split('/')[-1]}")
    df_in = pd.read_csv(f)
    data = np.array(df_in.Molecular_Weight)
    interval_files = getIntervalFiles()

    intervals = []
    for i in interval_files:
        name0 = i.strip(".csv").split('/')[-1]
        name1 = name0.split('_')
        intervals.append(name1)
    ints0 = np.array(intervals[1:], dtype=int)

    for i in ints0:
        path_this_interval = f"{path_csv_mass_intervals}/{i[0]}_{i[1]}.csv"

        try:
            #print(f"Adding to {i[0]}_{i[1]}.csv")
            indicies = np.where((i[0] <= data) & (data <= i[1] + overflow))
            matches = df_in[indicies[0][0] : indicies[0][-1] + 1]
        except:
            pass

        matches.to_csv(path_this_interval, mode='a', header=False, index=False)


def sortInterval(f):
    df_in = pd.read_csv(f)
    data = df_in.sort_values(by='Molecular_Weight')


def masterCsv(f):
    #skel_df = pd.DataFrame(columns=['Molecular_Formula', 'Molecular_Weight'])
    #skel_df.to_csv(path_master, mode='w', header=True, index=False)

    print(f"\nFor {f.split('/')[-1]}")
    in_df = pd.read_csv(f)
    #print(in_df)
    in_df.to_csv(path_master, mode='a', header=True, index=False)


class Master(object):
    def __init__(self):
        self.path = "/Users/etiennechollet/Desktop/GitHub/1A-Database/LexiChem/CSV_Master/master.csv"

    def refresh(self):
        skel_df = pd.DataFrame(columns=['Molecular_Formula', 'Molecular_Weight'])
        skel_df.to_csv(self.path, mode='w', header=True, index=False)

    def updateFrom(self, f):
        print(f"\nFor {f.split('/')[-1]}")
        in_df = pd.read_csv(f)
        #print(in_df)
        in_df.to_csv(self.path, mode='a', header=False, index=False)

    def sort(self):
        in_df = pd.read_csv(self.path)
        out_df = in_df.sort_values(by=['Molecular_Weight'])
        out_df.to_csv(self.path, mode='w', header=True, index=False)
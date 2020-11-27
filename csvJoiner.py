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


def sortInterval(f):
    df_in = pd.read_csv(f)
    data = df_in.sort_values(by='Molecular_Weight')


class Master(object):
    def __init__(self):
        self.path = "/Users/etiennechollet/Desktop/GitHub/1A-Database/LexiChem/CSV_Master/master.csv"

    def refresh(self):
        skel_df = pd.DataFrame(columns=['Molecular_Formula', 'Molecular_Weight'])
        skel_df.to_csv(self.path, mode='w', header=True, index=False)

    def writer(self, f):
        print(f"\nFor {f.split('/')[-1]}")
        in_df = pd.read_csv(f)
        #print(in_df)
        in_df.to_csv(self.path, mode='a', header=False, index=False)

    def sort(self):
        in_df = pd.read_csv(self.path)
        out_df = in_df.sort_values(by=['Molecular_Weight'])
        out_df.to_csv(self.path, mode='w', header=True, index=False)


class Intervals(object):
    def __init__(self):
        self.path = "/Users/etiennechollet/Desktop/GitHub/1A-Database/LexiChem/CSV_Mass_Intervals"

    def intervalLimits(self):
        subintervals = []
        nodes = np.arange(0, 5200, 200)
        for i in range(len(nodes)):
            subinterval = nodes[i : i + 2]
            subintervals.append(list(subinterval))
    
        subintervals.pop()
        subintervals.append([5000, 50000])
        return subintervals

    def files(self):
        fs = []
        for dirpath, dirnames, filenames in os.walk(self.path):
            for i in filenames:
                fs.append(f"{self.path}/{i}")

        sorted_files = sorted(fs)
        sorted_files.pop(0)
        return sorted_files
        
    def refreshAll(self):
        df = pd.DataFrame(columns=['Molecular_Formula', 'Molecular_Weight'])
        for subinterval in self.intervalLimits():
            a = subinterval[0]
            b = subinterval[1]
            csv_name = f"{a}_{b}.csv"
            df.to_csv(f'{self.path}/{csv_name}', mode='w', header=True, index=False)
            print(f'Made {csv_name}')

    def writer(self, f, overflow):
        print(f"\nFor {f.split('/')[-1]}")
        df_in = pd.read_csv(f)
        data = np.array(df_in.Molecular_Weight)
        interval_files = self.files()

        intervals = []
        for i in interval_files:
            name0 = i.strip(".csv").split('/')[-1]
            name1 = name0.split('_')
            intervals.append(name1)
        ints0 = np.array(intervals[1:], dtype=int)

        for i in ints0:
            path_this_interval = f"{self.path}/{i[0]}_{i[1]}.csv"

            try:
                #print(f"Adding to {i[0]}_{i[1]}.csv")
                indicies = np.where((i[0] <= data) & (data <= i[1] + overflow))
                matches = df_in[indicies[0][0] : indicies[0][-1] + 1]
                matches.to_csv(path_this_interval, mode='w', header=False, index=False)
            except:
                pass

            
class Split(object):
    def __init__(self):
        self.path = "/Users/etiennechollet/Desktop/GitHub/1A-Database/LexiChem/CSV_Splits"
    
    def getFilenames(self):
        files = []
        for dirpath, dirnames, filenames in os.walk(path_csv_splits):
            for i in filenames:
                files.append(f"{path_csv_splits}/{i}")

        sorted_files = sorted(files)
        sorted_files.pop(0)
        return sorted_files

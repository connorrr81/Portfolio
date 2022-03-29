# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 10:43:48 2021

@author: CLaug
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path
import pandas as pd

def get_species_tree():
    #ids = geneticStrings.keys()
    
    # Load phylogenetic tree
    ROOTPATH = Path('C:/Users/CLaug/Documents/toDukeFromBold')
    DATAPATH = ROOTPATH.joinpath('animalia')
    TREEFILE = DATAPATH.joinpath('BINs_taxCounts.txt')
    
    df = pd.read_csv(TREEFILE, delimiter='\t', header=None)
    df.rename(columns = {0:'BOLD_ID',
                         1:'Phylum',
                         2:'Class',
                         3:'Order',
                         4:'Family',
                         5:'Genus',
                         6:'Species'}, 
              inplace = True)
    df["BOLD_ID"] = df["BOLD_ID"].str[-12:]
    df = df.set_index('BOLD_ID')
    return df

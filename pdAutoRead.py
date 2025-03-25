#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 12:25:26 2022

@author: dan.budden
"""

def pdAutoRead(filepath):
    """
    Detects filetype based on string, and uses pandas.read_* to ingest
    Returns pandas df
    """
    import pandas as pd
    
    if filepath[-4:] == ".xls":
        output = pd.read_excel(filepath, engine="xlrd")
    elif filepath[-5:] == ".xlsx":
        output = pd.read_excel(filepath, engine="openpyxl")
    elif filepath[-4:] == ".csv":
        output = pd.read_csv(filepath)
    elif filepath[-7:] == ".pickle":
        output = pd.read_pickle(filepath)
    else:
        raise ValueError("Check format is: xls, xlsx, csv, pickle")

    return output
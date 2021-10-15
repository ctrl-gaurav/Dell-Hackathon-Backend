import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
try:
    from PIL import image
except ImportError:
    import image 
import pytesseract

def merge():
    path = "GridCSVs"
    file_list = glob.glob(path + "/*.xlsx")
    excl_list = []

    for file in file_list:
        excl_list.append(pd.read_excel(file))

    
    excl_merged = pd.DataFrame()

    for excl_file in excl_list:
        excl_merged = excl_merged.append(excl_file, ignore_index=True)
    excl_merged.to_excel("output.xlsx", index=False)

merge()
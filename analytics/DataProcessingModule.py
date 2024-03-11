import pandas as pd 
import numpy as np 


def clean_dataframe(df: pd.DataFrame):
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if df.iloc[i , j] == "-":
                df.iloc[i , j] = None
    

